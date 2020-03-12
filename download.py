import urllib.request
import os
import argparse
import errno
import pandas as pd
from tqdm import tqdm
from multiprocessing.pool import ThreadPool
from time import time as timer
#
#
# data_type = 'train'
# # data_type = 'test'
# data_folder = os.path.join('data', data_type)
# img_file = 'test-images.csv' if data_type == 'test' else 'train-images-boxable.csv'
#
# argparser = argparse.ArgumentParser(description='Download specific objects from Open-Images dataset')
# argparser.add_argument('-a', '--annots',
#                        help='path to annotations file (.csv)',
#                        default=os.path.join(data_folder, '{}-annotations-bbox.csv'.format(data_type)))
# argparser.add_argument('-o', '--objects', nargs='+',
#                        help='download images of these objects')
# argparser.add_argument('-d', '--dir',
#                        help='path to output directory',
#                        default='images')
# argparser.add_argument('-l', '--labelmap',
#                        help='path to labelmap (.csv)',
#                        default='data/class-descriptions-boxable.csv')
# argparser.add_argument('-i', '--images',
#                        help='path to file containing links to images (.csv)',
#                        default=os.path.join(data_folder,
#                                             img_file))
# argparser.add_argument('--limit', type=int,
#                        default=50)
#
# args = argparser.parse_args()
#
# # parse arguments
# ANNOTATIONS = args.annots
# print('ANNOTATIONS= {}'.format(ANNOTATIONS))
# OUTPUT_DIR = args.dir
# print('OUTPUT_DIR= {}'.format(OUTPUT_DIR))
# OBJECTS = args.objects
# print('OBJECTS= {}'.format(OBJECTS))
# LABELMAP = args.labelmap
# print('LABELMAP= {}'.format(LABELMAP))
# IMAGES = args.images
# print('IMAGES= {}'.format(IMAGES))
#
# # make OUTPUT_DIR if not present
# if not os.path.isdir(OUTPUT_DIR):
#     os.makedirs(OUTPUT_DIR)
#     print("\nCreated {} directory\n".format(OUTPUT_DIR))
#
# # check if input files are valid, raise FileNotFoundError if not found
# if not os.path.exists(ANNOTATIONS):
#     raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), ANNOTATIONS)
# elif not os.path.exists(LABELMAP):
#     raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), LABELMAP)


def get_ooi_labelmap(labelmap):
    '''
    Given labelmap of all objects in Open Images dataset, get labelmap of objects of interest
    :param labelmap: dataframe containing object labels with respective label codes
    :return: dictionary containing object labels and codes of
                          user-inputted objects
    '''

    object_codes = {}

    for idx, row in labelmap.iterrows():
        for obj in OBJECTS:
            if obj.lower() == row[1].lower():
                print('{} {}'.format(row[1], obj.lower()))
                object_codes[row[1].lower()] = row[0]

    # for idx, row in labelmap.iterrows():
    #     if any(obj.lower() in row[1].lower() for obj in OBJECTS):
    #         object_codes[row[1].lower()] = row[0]

    return object_codes


def generate_download_list(annotations, labelmap, base_url, args, data_type):
    '''
    Parse through input annotations dataframe, find ImageID's of objects of interest,
    and get download urls for the corresponding images
    :param annotations: annotations dataframe
    :param labelmap: dictionary of object labels and codes
    :param base_url: basename of url
    :return: list of urls to download
    '''
    # create an empty dataframe
    df_download = pd.DataFrame(columns=['ImageID', 'LabelName'])

    for key, value in labelmap.items():
        aaa = annotations.loc[annotations['LabelName'] == value, ['ImageID', 'LabelName']].head(args.limit)
        print('For class {} in {} found: {} pic. limit to: {}'.format(key, data_type, aaa.shape[0], args.limit))
        df_download = df_download.append(aaa)

    url_download_list = []

    for idx, row in df_download.iterrows():
        # get name of the image
        image_name = row['ImageID'] + ".jpg"

        # check if the image exists in directory
        if not os.path.exists(os.path.join(OUTPUT_DIR, image_name)):
            # form url
            url = os.path.join(base_url, image_name)
            url_download_list.append((url, row['LabelName']))
            # url_download_list.append(url)

    print('666 - len of url_download_list : {}'.format(len(url_download_list)))
    return url_download_list


def download_objects_of_interest(download_list):
    def fetch_url(url):
        try:
            print(url)
            image_name = url[0].split("/")[-1].split('.')
            urllib.request.urlretrieve(url[0], os.path.join(OUTPUT_DIR, '{}_{}.{}'.format(image_name[0], class_code_to_class_name[url[1]], image_name[1])))
            return url[0], None
        except Exception as e:
            return None, e


    start = timer()
    results = [fetch_url(x) for x in download_list]
    df_pbar = tqdm(total=len(download_list), position=1, desc="Download %: ")

    print('results len: {}'.format(len(results)))
    for url, error in results:
        df_pbar.update(1)
        if error is None:
            pass  # TODO: find a way to do tqdm.write() with a refresh
            # print("{} fetched in {}s".format(url, timer() - start), end='\r')
        else:
            print('Error accrued')
            pass  # TODO: find a way to do tqdm.write() with a refresh
            # print("error fetching {}: {}".format(url, error), end='\r')


def main():
    data_types = ['train', 'test']
    for data_type in data_types:
        data_folder = os.path.join('data', data_type)
        img_file = 'test-images.csv' if data_type == 'test' else 'train-images-boxable.csv'

        # notice: args ex: --limit 2 --objects alpaca armadillo axe balloon barrel beaker belt bomb beetle fax cello bat binoculars bee
        argparser = argparse.ArgumentParser(description='Download specific objects from Open-Images dataset')
        argparser.add_argument('-a', '--annots',
                               help='path to annotations file (.csv)',
                               default=os.path.join(data_folder, '{}-annotations-bbox.csv'.format(data_type)))
        argparser.add_argument('-o', '--objects', nargs='+',
                               help='download images of these objects')
        argparser.add_argument('-d', '--dir',
                               help='path to output directory',
                               default='images')
        argparser.add_argument('-l', '--labelmap',
                               help='path to labelmap (.csv)',
                               default='data/class-descriptions-boxable.csv')
        argparser.add_argument('-i', '--images',
                               help='path to file containing links to images (.csv)',
                               default=os.path.join(data_folder,
                                                    img_file))
        argparser.add_argument('--limit', type=int, default=100)
        argparser.add_argument('--run_local', default=False, action='store_true')

        args = argparser.parse_args()



        global ANNOTATIONS, OUTPUT_DIR, OBJECTS, LABELMAP, IMAGES, class_code_to_class_name

        file_name = 'data/class-descriptions-boxable.csv'
        class_code_to_class_name = dict()
        rev_class_code_to_class_name = dict()

        # Map class to code
        import csv
        with open(file_name) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                class_code_to_class_name[row[0]] = row[1]
                rev_class_code_to_class_name[row[1]] = row[0]


        # parse arguments
        ANNOTATIONS = args.annots
        print('ANNOTATIONS= {}'.format(ANNOTATIONS))
        OUTPUT_DIR = 'images' if args.run_local else '/yoav_stg/gshalev/semantic_labeling/cifar100_gen/images'
        print('OUTPUT_DIR= {}'.format(OUTPUT_DIR))
        OBJECTS = args.objects #NOTICE : the objects to download
        print('OBJECTS= {}'.format(OBJECTS))
        LABELMAP = args.labelmap
        print('LABELMAP= {}'.format(LABELMAP))
        IMAGES = args.images
        print('IMAGES= {}'.format(IMAGES))

        # make OUTPUT_DIR if not present
        if not os.path.isdir(OUTPUT_DIR):
            os.makedirs(OUTPUT_DIR)
            print("\nCreated {} directory\n".format(OUTPUT_DIR))

        # check if input files are valid, raise FileNotFoundError if not found
        if not os.path.exists(ANNOTATIONS):
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), ANNOTATIONS)
        elif not os.path.exists(LABELMAP):
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), LABELMAP)


        # read images and get base_url
        print('IMAGES = {}'.format(IMAGES))
        df_images = pd.read_csv(IMAGES)
        base_url = os.path.dirname(df_images['image_url'][0])  # used to download the images

        # read labelmap
        df_oid_labelmap = pd.read_csv(LABELMAP)  # open images dataset (oid) labelmap
        ooi_labelmap = get_ooi_labelmap(df_oid_labelmap)  # objects of interest (ooi) labelmap

        # read annotations
        df_annotations = pd.read_csv(ANNOTATIONS)

        print("\nGenerating download list for the following objects: ", [k for k, v in ooi_labelmap.items()])

        # get url list to download
        download_list = generate_download_list(annotations=df_annotations,
                                               labelmap=ooi_labelmap,
                                               base_url=base_url,
                                               args=args,
                                               data_type=data_type)

        # download objects of interest
        download_objects_of_interest(download_list)

        print("\nFinished downloads.")


if __name__ == '__main__':
    main()
# download.py
