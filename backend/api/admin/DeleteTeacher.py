#Author:Elin 
#Create Time:2023-02-08 16:23:30
#Last Modified By:Elin
#Update Time:2023-02-08 16:23:30
  
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

def deleteTeacher(teacher_id):
    excute_sql = f"""
    DELETE FROM TEACHER WHERE TEACHER_ID = '{teacher_id}';
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