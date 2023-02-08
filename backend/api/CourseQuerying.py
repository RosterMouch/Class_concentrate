#Author: Elin
#Date: 2023-01-17 11:49:06
 #Last Modified by:   Elin 
 #Last Modified time: 2023-01-17 11:49:06 
import pymysql as sql
from hashlib import md5
import json

config = json.load(open('../config/db.json', 'r'))
ip = config['server']['ip']
db = config['database']['db']
user = config['database']['user']
password = config['database']['pwd']
charset = config['database']['charset']



def courseQuerying(teacher_id):
    con = sql.connect(host=ip, user=user, password=password, db=db, charset=charset)
    cursor = con.cursor()

    excute_sql = f"""
    SELECT * FROM course
    where teacher_id = {teacher_id};
    """

    cursor.execute(excute_sql)

    result = cursor.fetchall()
    daySwitcher = lambda x:"周一" if x == 1 else "周二" if x == 2 else "周三" if x == 3 else "周四" if x == 4 else "周五" if x == 5 else "周六" if x == 6 else "周日"
    response = []
    for i in range(len(result)):
        # course_id.append(result[i][0])
        # course_name.append(result[i][2])
        # course_class.append(result[i][4])
        # course_major.append(result[i][5])
        # course_grade.append(result[i][6])
        # course_begin.append(result[i][7])
        # course_end.append(result[i][8])
        # course_week.append(result[i][9])
        respBody = {
            "course_id": result[i][0],
            "course_name": result[i][2],
            "course_class": result[i][4],
            "course_major": result[i][5],
            "course_grade": result[i][6],
            "course_begin": result[i][7],
            "course_end": result[i][8],
            "course_day": daySwitcher(result[i][9])
        }
        response.append(respBody)
    con.close()
    return response

if __name__ == "__main__":
    print(courseQuerying(1))