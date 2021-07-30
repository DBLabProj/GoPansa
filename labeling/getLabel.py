import cv2
import qrcode
import numpy as np
import pymysql
from PIL import ImageFont, ImageDraw, Image


# connect to local mysql server
# input: no
# output: database
def connect_db():
    db = pymysql.connect(
    user='root', 
    passwd='3520', 
    host='127.0.0.1',
    db='classify_meat', 
    charset='utf8')
    
    return db

# get data that is filtered by id from database
# input: 'no' in classify_meat record you want to find
# output: result(dictionary)
def get_label_data(no):
    db = connect_db()
    cursor = db.cursor(pymysql.cursors.DictCursor)

    sql = "\
    SELECT  c.no, c.datetime, u.name, c.meat_type, c.grade\
    FROM    user u, classify c\
    WHERE   no = '" + no + "'"

    cursor.execute(sql)

    result = cursor.fetchone()
    result['datetime'] = str(result['datetime'])

    return result

# create label based on 'no' value
# input: 'no' values
# output: label image file
def create_label(no):
    classify_info = get_label_data(no)
    no = classify_info["no"]
    datetime =  classify_info["datetime"]
    name = classify_info["name"]
    meat_type = classify_info["meat_type"]
    grade = classify_info["grade"]

    title_font = ImageFont.truetype("./static/fonts/ONE Mobile Bold.ttf", 18)
    content_font = ImageFont.truetype("./static/fonts/ONE Mobile Regular.ttf", 12)
    grade_font = ImageFont.truetype("./static/fonts/GmarketSansTTFBold.ttf", 36)

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
    print(width, height)
    draw.text((img_width - (width + padding), padding), grade, font=grade_font, fill=(0,0,0))

    # qr code draw
    qr_code = qr_code.resize((qrcode_size, qrcode_size))
    img.paste(im=qr_code, box=((img_width-(qrcode_size + padding)), (img_height-(qrcode_size + padding))))

    img = np.array(img)

    cv2.imshow("text", img)

    cv2.waitKey()
    cv2.destroyAllWindows()


create_label('210729-B1462')