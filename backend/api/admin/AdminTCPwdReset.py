#Author:Elin 
#Create Time:2023-02-08 10:47:04
#Last Modified By:Elin
#Update Time:2023-02-08 10:47:04
import pymysql as sql
from hashlib import sha256
import json

config = json.load(open('../config/db.json', 'r'))
ip = config['server']['ip']
db = config['database']['db']
user = config['database']['user']
password = config['database']['pwd']
charset = config['database']['charset']

con = sql.connect(host=ip, user=user, password=password, db=db, charset=charset)

def resetTCPwd(
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