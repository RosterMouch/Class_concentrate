#Author:Elin 
#Create Time:2023-02-08 16:33:13
#Last Modified By:Elin
#Update Time:2023-02-08 16:33:13
import pymysql as sql
from hashlib import md5
import json
config = json.load(open('../config/db.json', 'r'))
ip = config['server']['ip']
db = config['database']['db']
user = config['database']['user']
password = config['database']['pwd']
charset = config['database']['charset']

con = sql.connect(host=ip, user=user, password=password, db=db, charset=charset)

def addStudent(
    student_name,
    student_class,
    student_grade,
    student_major,    
):
    student_password = md5("123456".encode('utf-8')).hexdigest()
    excute_sql = f"""
    INSERT INTO STUDENT(student_name,student_class,student_grade,student_major,student_password) VALUES('{student_name}','{student_class}','{student_grade}','{student_major}','{student_password}');
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