import csv
import json


file_name = 'class-descriptions-boxable.csv'
class_code_to_class_name = dict()

with open(file_name) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        class_code_to_class_name[row[0]] = row[1]

with open('bbox_labels_600_hierarchy.json.csv') as f:
    content = json.load(f)
    to_take_care = [content]

    while len(to_take_care) > 0:
        current_node = to_take_care.pop(0)

        if current_node['LabelName'] in class_code_to_class_name:
            current_node['LabelName'] = class_code_to_class_name[current_node['LabelName']]

        if 'Subcategory' in current_node:
            for child in current_node['Subcategory']:
                to_take_care.append(child)

    with open('result.json', 'w') as fp:
        json.dump(content, fp)
