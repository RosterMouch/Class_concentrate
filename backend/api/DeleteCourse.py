#Author: Elin
#Date: 2023-01-24 10:47:09
 #Last Modified by:   Elin 
 #Last Modified time: 2023-01-24 10:47:09 
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
con.autocommit(True)
def DeleteCourse(
    course_id,
):
    cursor = con.cursor()
    runSucess = None
    excute_sql = [
    "set foreign_key_checks = 0;",
    f"DELETE FROM course WHERE course_id = {course_id};",
    "set foreign_key_checks = 1;"]
    for i in range(len(excute_sql)):
        cursor.execute(excute_sql[i])
        if i == 1:
            if cursor.rowcount == 1:
                runSucess = True
            else:
                runSucess = False
    return runSucess
