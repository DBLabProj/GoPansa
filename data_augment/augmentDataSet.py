'''
# 21.07.29
# data set augment 
'''
import glob, os
from augmentImage import *
from augmentJson import *

source_dir = "D:/data_set/meat_data/training/"
target_dir = "D:/data_set/meat_data/training/"

image_augmentor(source_dir, target_dir, v=True, h=True, r=False)

'''
os.chdir(source_dir)
count = 1
for json_file in glob.glob("*.json"):
    augment_json_data(json_file, method="h", path="./")
    augment_json_data(json_file, method="v", path="./")
    count+=1

    if count % 3000 == 0 :
        print(count)

'''
# image_augmentor(input_path, v=True, h=True, r=True)
# augment_json_data(file_name, method="h", path="./")

