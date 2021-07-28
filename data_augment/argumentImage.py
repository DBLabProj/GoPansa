import time
import os
from PIL import Image
import sys

def image_augmentor(input_path, v=True, h=True, r=True):
    print("Process Start.")

    # start_time = time.time()

    # 결과 저장 폴더 생성
    out_dir ="augmentation"
    if out_dir not in os.listdir():
        os.mkdir(out_dir)
    
    for filename in os.listdir(folder):
        image = None
        if ".png" in filename.lower() or ".jpg" in filename.lower():
            image = Image.open(folder+"/"+filename)
            if image is None:
                continue
                
        Xdim, Ydim = image.size

        # 좌우대칭
        if h:
            # 변환된 파일을 저장하기 위해 새로운 이름을 지정
            new_temp_name = f"h_{filename}"
            
            # 이미지를 좌우 반전
            image = image.transpose(Image.FLIP_LEFT_RIGHT)
            
            # 좌우 반전된 이미지를 저장
            image.save(out_dir + "/" + new_temp_name)

        # 상하대칭
        if v:
            # 변환된 파일을 저장하기 위해 새로운 이름을 지정
            new_temp_name = f"v_{filename}"
            
            # 이미지를 상하 반전
            image = image.transpose(Image.FLIP_TOP_BOTTOM)
            
            # 상하 반전된 이미지를 저장
            image.save(out_dir + "/" + new_temp_name)


        # 180도 회전
        if r:
            # 변환된 파일을 저장하기 위해 새로운 이름을 지정
            new_temp_name = f"r_{filename}"
            
            #  사진180도 회전
            image = image.rotate(180)
            
            # 간혹 이미지 크기가 변경된다는 이야기가 있어 resize()를 실행합니다.
            image = image.resize((Xdim, Ydim))
            
            # 회전 된 이미지를 저장
            image.save(out_dir + "/" + new_temp_name)
        image.close()

    print("Process Done.")

    # end_time = time.time()
    # print("The Job Took " + str(end_time - start_time) + " seconds.")


input_path = "D:/지용/python/workspace/ai/test/data"
image_augmentor(input_path, v=True, h=True, r=True)