#Author:Elin 
#Create Time:2023-02-08 15:40:55
#Last Modified By:Elin
#Update Time:2023-02-08 15:40:55
  
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

def addTeacher(teacher_name):
    pwd = sha256("123456".encode('utf-8')).hexdigest()
    excute_sql = f"""
    INSERT INTO TEACHER(TEACHER_NAME,TEACHER_PASSWORD) VALUES("{teacher_name}","{pwd}");
    """
    cursor = con.cursor()
    cursor.execute(excute_sql)
    if cursor.rowcount == 1:
        con.commit()
        con.close()
        return True
    else:
        con.close()
        return False