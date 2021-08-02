
import os, json


# 해당 폴더 내 모든 json 파일 읽어서
# 이미지 사이즈의 최솟값 최댓값을 알아냄
# 좀 오래 걸림
def getJsonList(path):
    width = [10000, 0]
    height = [10000, 0]

    for index, filename in enumerate( os.listdir(path) ):
        
        if ".json" in filename.lower():
            print(filename)
            with open(f"{path}{filename}", 'rt') as f:
                json_data = json.load(f)

            w=json_data['label_info']['image']['width']
            h=json_data['label_info']['image']['height']

            if w < width[0]: width[0] = w
            elif w > width[1] : width[1] = w

            if h < height[0] : height[0] = h
            elif h > height[1]: height[1] = h

    return width, height

if __name__ == "__main__":
    path = "D:/data_set/meat_data/training/"
    w, h = getJsonList(path)
    print(w)
    print(h)


    pass