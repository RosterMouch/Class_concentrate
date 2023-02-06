#Author: Elin
#Date: 2023-01-15 11:53:27
 #Last Modified by:   Elin 
 #Last Modified time: 2023-01-15 11:53:27 
import pymysql as sql
from hashlib import md5
import json
from datetime import datetime

config = json.load(open('../config/db.json', 'r'))
ip = config['server']['ip']
db = config['database']['db']
user = config['database']['user']
password = config['database']['pwd']
charset = config['database']['charset']

con = sql.connect(host=ip, user=user, password=password, db=db, charset=charset)

def courseQuerying(student_id):
    cursor = con.cursor()
    day = datetime.now().ctime().split(' ')[0]
    hour = int(datetime.now().ctime().split(' ')[4].split(':')[0])
    minute = int(datetime.now().ctime().split(' ')[4].split(':')[1])
    excute_sql = f"""
    SELECT * FROM course
    WHERE course_class = (SELECT student_class from STUDENT WHERE student_id = {student_id})
    AND course_major = (SELECT student_major from STUDENT WHERE student_id = {student_id})
    AND course_grade = (SELECT student_grade from STUDENT WHERE student_id = {student_id})
    AND course_date  = "{day}";
    """
    cursor.execute(excute_sql)
    daySwitcher = lambda x:"周一" if x == 'Mon' else "周二" if x == 'Tue' else "周三" if x == 'Wed' else "周四" if x == 'Thu' else "周五" if x == 'Fri' else "周六" if x == 'Sat' else "周日"
    result = cursor.fetchall()
    for i in range(len(result)):
        if day == result[i][-1]:
            courseBeginHour = int(result[i][7].split(':')[0])
            courseBeginMin = int(result[i][7].split(':')[1])
            if hour <= courseBeginHour - 1:
                respBody = {
                    "course_name":result[i][2],
                    "course_teacher":result[i][3],
                    "course_begin":result[i][7],
                    "course_end":result[i][8],
                    "course_day":daySwitcher(result[i][9]),
                    "classroom":True
                }
                return respBody
            elif hour == courseBeginHour:
                if minute < courseBeginMin:
                    respBody = {
                    "course_name":result[i][2],
                    "course_teacher":result[i][3],
                    "course_begin":result[i][7],
                    "course_end":result[i][8],
                    "course_day":daySwitcher(result[i][9]),
                    "classroom":True
                    }
                    return respBody
                elif minute <= courseBeginMin + 10:
                    respBody = {
                    "course_name":result[i][2],
                    "course_teacher":result[i][3],
                    "course_begin":result[i][7],
                    "course_end":result[i][8],
                    "course_day":daySwitcher(result[i][9]),
                    "classroom":True
                    }
                    return respBody
            else:
                pass
        else:
            return None
