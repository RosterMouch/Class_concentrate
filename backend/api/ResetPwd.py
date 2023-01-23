#Author: Elin
#Date: 2023-01-23 13:56:44
 #Last Modified by:   Elin 
 #Last Modified time: 2023-01-23 13:56:44 
import pymysql as sql
from hashlib import sha256
import json
from pymysql.err import InterfaceError

config = json.load(open('../config/db.json', 'r'))
ip = config['server']['ip']
db = config['database']['db']
user = config['database']['user']
password = config['database']['pwd']
charset = config['database']['charset']
con = sql.connect(host=ip, user=user, password=password, db=db, charset=charset)

def resetPwd(
    teacher_id,old_pwd,new_pwd
):
    cursor = con.cursor()

    excute_sql = f"""
    UPDATE TEACHER set TEACHER_PASSWORD = "{sha256(new_pwd.encode('utf-8')).hexdigest()}"
    WHERE TEACHER_ID = {teacher_id} AND TEACHER_PASSWORD = "{sha256(old_pwd.encode('utf-8')).hexdigest()}"; 
    """
    cursor.execute(excute_sql)
    con.commit()
    if cursor.rowcount == 1:
        con.close()
        return True
    else:
        con.close()
        return False