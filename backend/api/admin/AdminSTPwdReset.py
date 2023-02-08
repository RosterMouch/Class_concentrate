#Author:Elin 
#Create Time:2023-02-08 12:13:57
#Last Modified By:Elin
#Update Time:2023-02-08 12:13:57
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

def resetSTPwd(
    student_id,old_pwd,new_pwd
):
    cursor = con.cursor()

    excute_sql = f"""
    UPDATE STUDENT set student_password = "{sha256(new_pwd.encode('utf-8')).hexdigest()}"
    WHERE student_id = {student_id} AND student_password = "{sha256(old_pwd.encode('utf-8')).hexdigest()}"; 
    """
    cursor.execute(excute_sql)
    con.commit()
    if cursor.rowcount == 1:
        con.close()
        return True
    else:
        con.close()
        return False