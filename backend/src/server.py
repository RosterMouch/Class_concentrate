#Author:Elin 
#Create Time:2023-02-08 10:15:37
#Last Modified By:Elin
#Update Time:2023-02-08 10:15:37
  

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
from api.DeleteCourse import DeleteCourse
from api.Summary import allRank
from api.admin.FetchTeacher import fetchTeacher
from api.admin.FetchStudent import fetchStudent
from api.admin.AdminTCPwdReset import resetTCPwd
from api.admin.AdminSTPwdReset import resetSTPwd
from api.admin.AddTeacher import addTeacher
from api.admin.DeleteTeacher import deleteTeacher
from api.admin.AddStudent import addStudent
from api.admin.DeleteStudent import deleteStudent
import requests as re
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
    print(request.cookies.get("teacher_id"))
    if request.cookies.get("teacher_id") == 1 or request.cookies.get("teacher_id") == "1":
        return render_template("admin.html")
    elif request.cookies.get("teacher_id") != None:
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

@app.route('/v1/teacher/deleteCourse',methods=['POST'])
def deleteCourse():
    data = request.get_json()
    course_id = data['course_id']
    result = DeleteCourse(course_id)
    resp = {
        'code':200,
        'msg':'success',
        'data':result
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
@app.route("/v1/teacher/allsummary",methods=['POST'])
def allrank():
    data = request.get_json()
    teacher_id = data['teacher_id']
    result = allRank(teacher_id)
    resp = {
        'code':200,
        'msg':'success',
        'data':result
    }
    return jsonify(resp)
@app.route("/v1/admin/fetchTeacher",methods=['GET'])
def fetch_teacher():
    if request.cookies.get("teacher_id") == 1 or request.cookies.get("teacher_id") == "1":
        result = fetchTeacher()
        resp = {
            'code':200,
            'msg':'success',
            'data':result
        }
        return jsonify(resp)
    else:
        return render_template("401.html")
@app.route("/v1/admin/fetchStudent",methods=['GET'])
def fetch_student():
    if request.cookies.get("teacher_id") == 1 or request.cookies.get("teacher_id") == "1":
        result = fetchStudent()
        resp = {
            'code':200,
            'msg':'success',
            'data':result
        }
        return jsonify(resp)
    else:
        return render_template("401.html")
@app.route("/v1/admin/resetTeacherPwd",methods=['POST'])
def reset_teacher_pwd():
    if request.cookies.get("teacher_id") == 1 or request.cookies.get("teacher_id") == "1":
        data = request.get_json()
        teacher_id = data['teacher_id']
        old_pwd = data['old_pwd']
        new_pwd = data['new_pwd']
        result = resetTCPwd(teacher_id,old_pwd,new_pwd)
        resp = {
            'code':200,
            'msg':'success',
            'data':result
        }
        return jsonify(resp)
    else:
        return render_template("401.html")
@app.route("/v1/admin/resetStudentPwd",methods=['POST'])
def reset_student_pwd():
    if request.cookies.get("teacher_id") == 1 or request.cookies.get("teacher_id") == "1":
        data = request.get_json()
        student_id = data['student_id']
        old_pwd = data['old_pwd']
        new_pwd = data['new_pwd']
        result = resetSTPwd(student_id,old_pwd,new_pwd)
        resp = {
            'code':200,
            'msg':'success',
            'data':result
        }
        return jsonify(resp)
    else:
        return render_template("401.html")
@app.route("/v1/admin/trtion",methods=['GET'])
def trtion():
    if request.cookies.get("teacher_id") == 1 or request.cookies.get("teacher_id") == "1":
        try:
            result = re.get("http://172.27.26.249:8000/v2/health/ready").status_code
        except:
            result = 500
        resp = {
            'code':200,
            'msg':'success',
            'data':result
        }
        return jsonify(resp)
    else:
        return render_template("401.html")
@app.route("/v1/admin/student-alive",methods=['GET'])
def student_alive():
    if request.cookies.get("teacher_id") == 0 or request.cookies.get("teacher_id") == "0":
        result = re.get("http://192.168.174.11:8080/v1/student/login")
        resp = {
            'code':200,
            'msg':'success',
            'data':result.status_code
        }
        return jsonify(resp)
    else:
        return render_template("401.html")
@app.route("/v1/admin/addTeacher",methods=['POST'])
def add_teacher():
    if request.cookies.get("teacher_id") == 1 or request.cookies.get("teacher_id") == "1":
        data = request.get_json()
        teacher_name = data['teacher_name']
        result = addTeacher(teacher_name)
        resp = {
            'code':200,
            'msg':'success',
            'data':result
        }
        return jsonify(resp)
    else:
        return render_template("401.html")
@app.route("/v1/admin/deleteTeacher",methods=['POST'])
def remove_teacher():
    if request.cookies.get("teacher_id") == 1 or request.cookies.get("teacher_id") == "1":
        data = request.get_json()
        teacher_id = data['teacher_id']
        result = deleteTeacher(teacher_id)
        resp = {
            'code':200,
            'msg':'success',
            'data':result
        }
        return jsonify(resp)
    else:
        return render_template("401.html")
@app.route("/v1/admin/addStudent",methods=['POST'])
def add_student():
    if request.cookies.get("teacher_id") == 1 or request.cookies.get("teacher_id") == "1":
        data = request.get_json()
        student_name = data['student_name']
        student_grade = data['student_grade']
        student_class = data['student_class']
        student_major = data['student_major']
        result = addStudent(student_name,student_grade,student_class,student_major)
        resp = {
            'code':200,
            'msg':'success',
            'data':result
        }
        return jsonify(resp)
    else:
        return render_template("401.html")
@app.route("/v1/admin/deleteStudent",methods=['POST'])
def remove_student():
    if request.cookies.get("teacher_id") == 1 or request.cookies.get("teacher_id") == "1":
        data = request.get_json()
        student_id = data['student_id']
        result = deleteStudent(student_id)
        resp = {
            'code':200,
            'msg':'success',
            'data':result
        }
        return jsonify(resp)
    else:
        return render_template("401.html")
if __name__ == '__main__':
    app.run(host=ip, port=port, debug=debug)
