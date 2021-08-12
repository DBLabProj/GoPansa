# flask server
# Author : minku Koo
# Project Start:: 2021.03.10
# Last Modified from Ji-yong 2021.06.11

from flask import Flask, request, render_template, jsonify, Blueprint, redirect, url_for, session, current_app
import os, json

import logging
from db.control_sql import Sql
from deeplearning_model.checkGrade import AIModel
from labeling.control_label import *
from raspberry import rasp_control
from .utils import *

views = Blueprint("server", __name__)
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

def get_id_name():
    id, name = '', ''

    if "id" in session:
        id = session["id"]
        if id is not None and id != "":
            name = getSql().get_data_from_db("name", "user", f"where id = '{id}'")[0]['name']

        else:
            id = ''

    return id, name


def getSql():
    return Sql( "203.252.240.74", 
                "classify_meat", 
                "dblab", 
                "dblab6100" )

@views.route("/", methods=["GET"])
def index():
    id, name = get_id_name()

    return render_template("index.html", id=id, name=name)

@views.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        if "id" in session:
            id = session["id"]
            if id and id != "":
                return redirect('/')

        return render_template("login.html", id='', name='')
        
    elif request.method == "POST":
        sql = getSql()
        id = request.form["id"]
        pw = request.form["pw"]
        result = sql.login( id, pw)
        
        if result == 1:
            session["id"] = id
                
            return redirect("/")

            
        elif result ==2:
            return "<script>alert('아이디가 존재하지 않습니다.');</script>"+render_template("login.html", id='')
            
        elif result == 3:
            return "<script>alert('비밀번호가 일치하지 않습니다.');</script>"+render_template("login.html", id='')
            
        elif result == 4:
            return "<script>alert('서비스 상태가 좋지 못합니다.\n다시 시도해주세요.');</script>"+render_template("login.html", id='')


@views.route("/logout", methods=["GET"])
def logout():
    session["id"] = None
    
    return redirect("/")


@views.route("/mypage", methods=["GET", "POST"])
def mypage():
    if request.method == "GET":
        id, name = get_id_name()

        if id != "":
            datas = getSql().get_data_from_db("name, main_store, phone, email, pw", "user", f"where id = '{id}'")[0]
            print(datas)
            datas['main_store'] = "" if datas['main_store'] == None else datas['main_store']
            
            if datas['phone'] == None: datas['phone'] = ""
            
            if len( datas['phone'] ) == 11:
                datas['phone'] = "".join( [x for x in datas['phone'][1:]] )
                datas['phone'] = '+82 ' + datas['phone'][:2] + "-" \
                                + datas['phone'][2]+"***-"+datas['phone'][6]+"***"
                                
            elif len( datas['phone'] ) == 0:
                datas['phone'] = "등록된 휴대폰이 없습니다."
            else:
                datas['phone'] = "존재하지 않는 번호"
                
            datas['pw'] = "".join( [ "*" for _ in datas['pw'] ] )
            return render_template("mypage.html", id=id, name=name, data=datas)

        else:
            return render_template("login.html", id=id, name=name)


@views.route("/findStore", methods=["POST"])
def findStore():
    store = request.form['store']
    
    sql = getSql()
    store_list = sql.getStoreList(store)
    
    return jsonify(result = store_list)

@views.route("/getStoreData", methods=["POST"])
def getStoreData():
    store_id = request.form['id']
    #print("store_id>",store_id)
    addr = getSql().getStoreAddr(store_id)
    return  jsonify(result = addr)

@views.route("/regist", methods=["GET", "POST"])
def regist():
    if request.method == "GET":
        id, name = get_id_name()
            
        return render_template("regist.html", id=id, name=name)
    
    elif request.method == "POST":
        id = request.form["ID"]
        pw = request.form["pass"]
        pwc = request.form["passck"]
        phone = request.form["PHONE"]
        username = request.form["username"]
        b_type = request.form["kinds"]
        b_name = request.form["store"]
        
        sql = getSql()
        result = sql.register(id, pw, username, phone)
                    
        if result == 2:
            return "<script>alert('이미 사용중인 아이디입니다.');</script>"+render_template("regist.html", id='')
        
        if pw != pwc:
            return "<script>alert('비밀번호를 다시 확인해주세요.');</script>"+render_template("regist.html", id='')
        
        if result == 3:
            return "<script>alert('비밀번호를 6자 이상 설정해주세요.');</script>"+render_template("regist.html", id='')
        
        if result == 4:
            return "<script>alert('서비스 상태가 좋지 못합니다.다시 시도해주세요.');</script>"+render_template("regist.html", id='')
        
        session["id"] = id
        return redirect('/')



@views.route("/check_label", methods=["POST"])
def check_label():
    label_code = request.form["code"]
    label_img = request.files["img"]

    print(f'label_text : {label_code}')
    print(f'label_img : {label_img.filename}')

    is_label_code = label_code == ""
    is_label_img = label_img.filename == ""

    err = False
    label_length = 12
    
    if not is_label_code:
        if len(label_code) != label_length:
            err = True
            print("length err")
        
        if not err:
            pass
            label_data = getSql().get_labeldata(label_code)
            
            print( "label_data",label_data )
        else:
            print("올바른 라벨 정보가 아닙니다.")
        
    elif not is_label_img:
        pass

    else:
        print("아무것도 안올림 에러")

    # 이미지 업로드 안했을 때
    if label_img.filename == "":
        pass

    return jsonify(data="success")
    
@views.route("/map", methods=["GET"])
def map():
    id, name = get_id_name()

    sql = Sql('203.252.240.74', 'classify_meat', 'dblab', 'dblab6100')
    store = sql.get_store()
    return render_template("map.html", store_list=store, id=id, name=name)
    
@views.route("/grade_table", methods=["GET"])
def grade_table():
    id, name = get_id_name()
    
    return render_template("grade_table.html", id=id, name=name)

@views.route("/check_grade", methods=["GET", "POST"])
def check_grade():
    if request.method == "GET":
        id, name = get_id_name()
        
        return render_template("check_grade.html", id=id, name=name)

    # elif request.method == "POST":
    #     rasp_control.shot_cam()
    #     rasp_control.get_img()
    #     return jsonify(data="success")

@views.route("/uploadIMG", methods=["POST"])
def upload_img():
    if 'file' not in request.files:
        resp = jsonify({'message' : 'No file part in the request'})
        resp.status_code = 400
        return resp

    files = request.files.getlist('file')
    meat_type = "pork"
    
    errors = {}
    success = False
    filepath = None

    for file in files:
        if file:
            # filename = secure_filename(file.filename) # secure_filename은 한글명을 지원하지 않음
            filename = file.filename 
            filepath = os.path.join("web/static/img/cam", filename)
            filepath = filepath.replace("\\", "/")
            # file_page_path = os.path.splitext(filepath)[0]
            
            # file save (with uploaded)
            file.save(filepath)
            success = True

        else:
            errors[file.filename] = 'File type is not allowed'
    
    if success and errors:
        errors['message'] = 'File(s) successfully uploaded'
        resp = jsonify(errors)
        resp.status_code = 206
        return resp

    # main 
    if success:
        grade = {
            "cow":{
                0: "1",
                1: "1+",
                2: "1++",
                3: "2",
                4: "3"
            },
            "pig":{
                0: "1+",
                1: "1",
                2: "2"
            }
        }
        print(f'filepath:{filepath}')
        model = AIModel()
        if meat_type == "beef":
            output, index = model.cow(filepath)
            result_grade = grade["cow"][index]

        elif meat_type == "pork":
            output, index = model.pig(filepath)
            result_grade = grade["pig"][index]
        
        print(f'result_grade : {result_grade}')

        resp = jsonify({'result' : result_grade})
        resp.status_code = 201

        sql = getSql()
        id, name = get_id_name()
        # print(id)
        result = sql.get_user_grade(id)
        print("result", result)
        
        if result  == "P":
            # id, name, filename, meat_type, result_grade
            meat_type_ = 'B' if meat_type == "beef" else "P"
            label_no = sql.insert_classify_data(id, filename, meat_type_, result_grade)
            
            # 여기에 디비 입력
            label_info = {
                "no": label_no,
                "datetime": getNowTime(),
                "name": name,
                "meat_type": meat_type,
                "grade": result_grade
            }
            create_label(label_info  )
            
            # 라벨 버튼 생성해주기
            
        else:
            print("프리미엄 고객 아님")

        return resp

    else:
        resp = jsonify(errors)
        resp.status_code = 400
        return resp