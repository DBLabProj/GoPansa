'''
21.07.29
'''
from shutil import copyfile
import os

# 이미지 디렉터리 이동
def move_image(source_dir, target_dir, included_name):
    for index, filename in enumerate( os.listdir(source_dir) ):
        if ".jpg" in filename.lower() and included_name in filename:
            copyfile(source_dir + filename, target_dir + filename)


if __name__ == "__main__":
    source_dir = "D:/data_set/meat_data/training/"
    target_dir = "D:/data_set/meat_data/gdrive_cow/training/"
    include = "cow"
    move_image(source_dir, target_dir, include)
