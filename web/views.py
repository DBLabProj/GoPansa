# flask server
# Author : minku Koo
# Project Start:: 2021.03.10
# Last Modified from Ji-yong 2021.06.11

from flask import Flask, request, render_template, jsonify, Blueprint, redirect, url_for, session, current_app
import os, json

import logging
from db.control_sql import Sql
from deeplearning_model.checkGrade import AIModel
from raspberry import rasp_control

views = Blueprint("server", __name__)
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

def get_id_name():
    id, name = '', ''
    
    if "id" in session:
        id = session["id"]
        if id and id != "":
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
            if "id" in session:
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


@views.route("/findStore", methods=["POST"])
def findStore():
    store = request.form['store']
    
    sql = getSql()
    store_list = sql.getStoreList(store)
    
    return jsonify(result = store_list)


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
                    
        if sql.is_id_exist(id):
            print("이미 사용중인 아이디입니다.")
            return  render_template("regist.html")
        
        if pw != pwc:
            print("비밀번호를 다시 확인해주세요.")
            return  render_template("regist.html")
        
        if not sql.register(id, pw, username, phone ):
            print("이미 사용중인 아이디입니다.")
            return  render_template("regist.html")
        
        # success
        if not sql.register(id, pw, username, phone, email=None):
            print("서비스 상태가 좋지 못합니다.\n다시 시도해주세요.")
            return  render_template("regist.html")
        
        if "id" not in session:
            session["id"] = get_job_id()
            pass
        return redirect('/')



@views.route("/check_label", methods=["POST"])
def check_label():
    label_code = request.form["tcodext"]
    label_img = request.files["img"]

    print(f'label_text : {label_code}')
    print(f'label_img : {label_img.filename}')

    is_label_code = label_code == ""
    is_label_img = label_img.filename == ""


    if is_label_code:
        pass

    elif is_label_img:
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

    elif request.method == "POST":
        rasp_control.shot_cam()
        rasp_control.get_img()
        return jsonify(data="success")

@views.route("/uploadIMG", methods=["POST"])
def upload_img():
    if 'file' not in request.files:
        resp = jsonify({'message' : 'No file part in the request'})
        resp.status_code = 400
        return resp

    files = request.files.getlist('file')

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
        output, index = model.cow(filepath)
        result_grade = grade["cow"][index]
        print(f'result_grade : {result_grade}')

        resp = jsonify({'result' : result_grade})
        resp.status_code = 201

        return resp

    else:
        resp = jsonify(errors)
        resp.status_code = 400
        return resp