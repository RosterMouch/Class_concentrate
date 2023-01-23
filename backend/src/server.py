#Author: Elin
#Date: 2023-01-17 12:01:21
 #Last Modified by:   Elin 
 #Last Modified time: 2023-01-17 12:01:21 

from flask import Flask,jsonify,request,render_template,make_response
from flask_cors import CORS
import os,sys
# 设置跨目录导入模块
current_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(current_path)
from api import CourseQuerying
from api.AuthCheck import auth_Check
from api.InsertCourse import InsertCourse
from api.ReplayQuery import ReplayQuery
from api.ResetPwd import resetPwd
import json

config = json.load(open("../config/server.json", "r"))
ip = config["bind_ip"]
port = config["port"]
debug = config["debug"]
app = Flask(__name__,template_folder="../../frontend/page",static_folder="../../frontend/static")
CORS(app)

@app.route("/index",methods=["GET"])
def login():
    return render_template("login.html")

@app.route("/dashboard",methods=["GET"])
def index():
    if request.cookies.get("teacher_id") != None:
        print(request.cookies.get("teacher_id"))
        return render_template("dashboard.html",teacher_name=request.cookies.get("teacher_name"),teacher_id=request.cookies.get("teacher_id"))
    else:
        return render_template("401.html")
@app.route("/v1/teacher/logout",methods=["GET"])
def logout():
    resp = make_response({"code":200,"msg":"success","data":True})
    resp.delete_cookie("teacher_id")
    resp.delete_cookie("teacher_name")
    return resp
@app.route("/v1/teacher/resetPwd",methods=["POST"])
def resetpwd():
    data = request.get_json()
    print(data)
    teacher_id = data["teacher_id"]
    old_pwd = data["old_pwd"]
    new_pwd = data["new_pwd"]
    result = resetPwd(teacher_id,old_pwd,new_pwd)
    resp = {
        "code":200,
        "msg":"success",
        "data":result
    }
    return jsonify(resp)


@app.route('/v1/teacher/login',methods=['POST'])
def authCheck():
    data = request.get_json()
    teacher_id = data['teacher_id']
    teacher_pwd = data['teacher_pwd']
    result = auth_Check(teacher_id,teacher_pwd)
    respBody = {
        'code':200,
        'msg':'success',
        'data':result
    }
    resp = make_response(jsonify(respBody))
    if result == "用户名或密码错误！":
        respBody['code'] = 500
        respBody['msg'] = 'fail'
    else:
        respBody['code'] = 200
        respBody['msg'] = 'success'
        respBody['data'] = result
        resp.set_cookie('teacher_id',teacher_id)
        resp.set_cookie('teacher_name',result[1])
    return resp


@app.route('/v1/teacher/courseQuerying',methods=['POST'])
def courseQuerying():
    data = request.get_json()
    teacher_id = data['teacher_id']
    result = CourseQuerying.courseQuerying(teacher_id)
    resp = {
        'code':200,
        'msg':'success',
        'data':result
    }
    return jsonify(resp)


@app.route('/v1/teacher/insertCourse',methods=['POST'])
def insertCourse():
    data = request.get_json()
    teacher_id = data['teacher_id']
    course_name = data['course_name']
    teacher_name = data['teacher_name']
    course_class = data['course_class']
    course_major = data['course_major']
    course_grade = data['course_grade']
    course_begin = data['course_begin']
    course_end = data['course_end']
    course_date = data['course_date']
    try:
        result = InsertCourse(
            teacher_id,course_name,teacher_name,
            course_class,course_major,course_grade,
            course_begin,course_end,course_date
        )
        resp = {
            'code':200,
            'msg':'success',
            'data':result
        }
    except Exception as e:
        resp = {
            'code':500,
            'msg':f'{str(e)})',
            'data':False
        }
    return jsonify(resp)

@app.route("/v1/teacher/replayQuery",methods=['POST'])
def replayQuery():
    data = request.get_json()
    teacher_id = data['teacher_id']
    result = ReplayQuery(teacher_id)
    resp = {
        'code':200,
        'msg':'success',
        'data':result
    }
    return jsonify(resp)

if __name__ == '__main__':
    app.run(host=ip, port=port, debug=debug)
