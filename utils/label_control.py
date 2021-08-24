import cv2
import qrcode
import numpy as np
from PIL import ImageFont, ImageDraw, Image
from db.control_sql import Sql
import os

# create label based on 'no' value
# input: 'no' values
# output: label image file
def create_label(classify_info):
    os.makedirs('./web/static/labels', exist_ok=True)
    no = classify_info["no"]
    datetime =  classify_info["datetime"]
    name = classify_info["name"]
    meat_type = classify_info["meat_type"]
    grade = classify_info["grade"]
    # print(os.getcwd())
    # print(os.listdir(os.getcwd()))
    content_font = ImageFont.truetype("web/static/font/ONE Mobile Regular.ttf", 12)
    grade_font = ImageFont.truetype("web/static/font/GmarketSansTTFBold.ttf", 36)
    title_font = ImageFont.truetype("web/static/font/ONE Mobile Bold.ttf", 18)
    img_width = 220
    img_height = 73
    padding = 5
    line_space = 1
    acc_y = 0.0 + padding
    qrcode_size = 25

    # canvas image
    img = Image.new("RGB", (img_width, img_height), color="#FFF")
    draw = ImageDraw.Draw(img)
    qr_code = qrcode.make(no)

    # create content
    content = [
        "일시:" + datetime,
        "측정자:" + name,
        "분류:" + meat_type,
    ]

    # draw title
    width, height = title_font.getsize(no)
    draw.text((padding, acc_y), no, font=title_font, fill=(0,0,0))
    # (line_space * 2) >> for separating between title and content
    acc_y += (height + (line_space * 2))

    # draw content
    for line in content:
        width, height = content_font.getsize(line)
        draw.text((padding, acc_y), line, font=content_font, fill=(0,0,0))
        acc_y += (height + line_space)

    # grade draw
    width, height = grade_font.getsize(grade)
    # print(width, height)
    draw.text((img_width - (width + padding), padding), grade, font=grade_font, fill=(0,0,0))

    # qr code draw
    qr_code = qr_code.resize((qrcode_size, qrcode_size))
    img.paste(im=qr_code, box=((img_width-(qrcode_size + padding)), (img_height-(qrcode_size + padding))))

    img = np.array(img)

    cv2.imwrite('./web/static/labels/' + no + '.png', img)


