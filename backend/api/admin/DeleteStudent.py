#Author:Elin 
#Create Time:2023-02-08 20:50:25
#Last Modified By:Elin
#Update Time:2023-02-08 20:50:25
  
  
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

def deleteStudent(student_id):
    cursor = con.cursor()
    runSucess = None
    excute_sql = [
    "set foreign_key_checks = 0;",
    f"""DELETE FROM STUDENT WHERE student_id = {student_id};""",
    "set foreign_key_checks = 1;"]
    for i in range(len(excute_sql)):
        cursor.execute(excute_sql[i])
        if i == 1:
            if cursor.rowcount == 1:
                con.commit()
                runSucess = True
            else:
                con.commit()
                runSucess = False
    return runSucess