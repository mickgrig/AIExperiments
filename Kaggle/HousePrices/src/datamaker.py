import csv

def file_to_data(file_name):
    with open(file_name) as file_obj:
        reader = csv.DictReader(file_obj, delimiter=',')
        for line in reader:
            print(line["Id"]),
            print(line["MSSubClass"])
    return [0, 0]