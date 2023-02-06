#Author: Elin
#Date: 2023-01-15 09:34:52
 #Last Modified by:   Elin 
 #Last Modified time: 2023-01-15 09:34:52 

import pymysql as sql
from hashlib import md5
import json

config = json.load(open("../config/db.json","r"))
server = config["server"]["ip"]
db = config["database"]["db"]
user = config["database"]["user"]
pwd = config["database"]["pwd"]
charset = config["database"]["charset"]

def auth_Check(student_id,student_pwd): 
    student_pwd_hash = md5(student_pwd.encode("utf-8")).hexdigest()
    excute_sql = f'select * from STUDENT where student_id = {student_id} and student_password = "{student_pwd_hash}";'
    try:
        connection = sql.connect(
            host=server,
            user=user,
            password=pwd,
            db=db,
            charset=charset
        )
        cursor = connection.cursor()
        cursor.execute(excute_sql)
        result = cursor.fetchall()
        if len(result) == 0:
            return "用户名或密码错误！"
        else:
            return result[0]
    except Exception:
        return "无法连接至数据库服务器！请联系网站管理员！"

