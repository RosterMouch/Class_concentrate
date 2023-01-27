#Author: Elin
#Date: 2023-01-19 18:43:04
 #Last Modified by:   Elin 
 #Last Modified time: 2023-01-19 18:43:04 


import pymysql as sql
from hashlib import md5
import json

config = json.load(open('../config/db.json', 'r'))
ip = config['server']['ip']
db = config['database']['db']
user = config['database']['user']
password = config['database']['pwd']
charset = config['database']['charset']



def ReplayQuery(
    teacher_id
):
    con = sql.connect(host=ip, user=user, password=password, db=db, charset=charset)
    cursor = con.cursor()

    excute_sql = f"""
    SELECT * FROM replay;
    """
    response = []
    cursor.execute(excute_sql)
    result = cursor.fetchall()
    for i in range(len(result)):
        resultBody = {
            "replay_id": result[i][0],
            "course_id": result[i][1],
            "student_id": result[i][2],
            "upload_time": result[i][3],
            "student_status": result[i][4],
            "replay_share_link": result[i][6]
        }
        response.append(resultBody)
    con.close()
    return response