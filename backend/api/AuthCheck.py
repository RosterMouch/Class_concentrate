#Author: Elin
#Date: 2023-01-17 11:44:43
#Last Modified by:   Elin 
#Last Modified time: 2023-01-17 11:44:43 

import pymysql as sql
from hashlib import sha256
import json

config = json.load(open("../config/db.json","r"))
server = config["server"]["ip"]
db = config["database"]["db"]
user = config["database"]["user"]
pwd = config["database"]["pwd"]
charset = config["database"]["charset"]

def auth_Check(teachert_id,teachert_pwd): 
    teachert_pwd_hash = sha256(teachert_pwd.encode("utf-8")).hexdigest()
    excute_sql = f'select TEACHER_ID,TEACHER_NAME from TEACHER where TEACHER_ID = {teachert_id} and TEACHER_PASSWORD = "{teachert_pwd_hash}";'
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
    except Exception as e:
        return str(e)