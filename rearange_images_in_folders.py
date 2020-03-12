import csv
import os
import shutil

file_name = 'train-annotations-bbox.csv'
# file_name = 'test-annotations-bbox.csv'

image_name_to_class_code = dict()
with open(file_name) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            line_count += 1
        else:
            image_name_to_class_code[row[0]] = row[2]



file_name = 'class-descriptions-boxable.csv'
class_code_to_class_name = dict()

with open(file_name) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
      class_code_to_class_name[row[0]] = row[1]
    # for row in csv_reader:
    #     print('class disc: {}   class: {}'.format(row[0], row[1]))


for img_name in os.listdir('images'):
    if 'jpg' in img_name:
        image_code = image_name_to_class_code[img_name.replace('.jpg', '')]
        image_class = class_code_to_class_name[image_code]
        path = os.path.join('images', image_class)

        if not os.path.exists(path):
            os.mkdir(path)
        shutil.move(os.path.join('images', img_name), os.path.join('images', image_class))

f = 0


# rearange_images_in_folders.py