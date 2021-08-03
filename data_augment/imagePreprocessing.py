'''
21.08.03

'''
from PIL import Image
import json
import cv2
import numpy as np


# 세그먼트 기준으로 이미지 잘라내기
def cropBySeg(image, point, padd = 5):
    ylist, xlist = [], []
    for x, y in point:
        ylist.append( int(y) )
        xlist.append( int(x) )

    crop_y, crop_x = [ min(ylist), max(ylist) ], [ min(xlist), max(xlist) ]
    
    w, h = crop_x[1]-crop_x[0], crop_y[1]-crop_y[0]

    cropped_image = image[ crop_y[0] - padd: crop_y[1] + padd , crop_x[0] - padd: crop_x[1] + padd ]
    return cropped_image, w, h

# image = image.rotate(180)
# 이미지를 세그먼트대로 잘라낸 다음, 세로로 변경
def preprocessing(imagepath, imagename, jsonpath, jsonname, saved_dir, pad = 10):
    with open(f"{jsonpath}{jsonname}.json", 'rt') as f:
        json_data = json.load(f)

    points = json_data['label_info']['shapes'][0]['points']

    image = cv2.imread(f'{imagepath}{imagename}.jpg', cv2.IMREAD_COLOR)
    cropped_image, w, h = cropBySeg(image, points, padd = pad)
    

    if w > h: # 가로 이미지
        cropped_image = cv2.rotate(cropped_image, cv2.ROTATE_90_CLOCKWISE)

    cv2.imwrite(saved_dir + "/" + imagename + "_crop.jpg", cropped_image)
    return 0
    
    
# 이미지 세그먼트 제대로되어있는지 확인
def checkSegShow(imagepath, imagename, jsonpath, jsonname):
    with open(f"{jsonpath}{jsonname}.json", 'rt') as f:
        json_data = json.load(f)
    
    points = json_data['label_info']['shapes'][0]['points']

    w=json_data['label_info']['image']['width']
    h=json_data['label_info']['image']['height']

    imshow_size = (w // 2, h // 2)
    
    image = cv2.imread(imagepath + imagename + ".jpg")

    for y, x in points:
        size = 10
        dot_color = [76, 88, 233]
        image[int(x)-size: int(x)+size, int(y)-size:int(y)+size] = np.array(dot_color)

    image = cv2.resize(image, imshow_size) 
    cv2.imshow("Image Segmentaion", image)
    cv2.waitKey(0)

    return 0


if __name__ == "__main__":
    impath = "./sample/pig/image/"
    jpath = "./sample/pig/seg/"

    imname = "QC_pig_segmentation_1_000004"
    jname = "QC_pig_segmentation_1_000004"

    savedd = "./sample/pig/croppedd/"

    # checkSegShow(impath, imname, jpath, jname)
    preprocessing(impath, imname, jpath, jname, savedd, pad = 0)
