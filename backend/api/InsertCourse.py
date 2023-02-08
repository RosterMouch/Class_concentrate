#Author: Elin
#Date: 2023-01-17 12:18:58
#Last Modified by:   Elin 
#Last Modified time: 2023-01-17 12:18:58 
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

def InsertCourse(
    teacher_id,course_name,teacher_name,
    course_class,course_major,course_grade,
    course_begin,course_end,course_date
):
    cursor = con.cursor()

    excute_sql = f"""
    INSERT INTO course(teacher_id,course_name,teacher_name,course_class,course_major,course_grade,course_begin,course_end,course_date)
    VALUE(
        '{teacher_id}','{course_name}','{teacher_name}',
        '{course_class}','{course_major}','{course_grade}',
        '{course_begin}','{course_end}','{course_date}'
    );
    """
    cursor.execute(excute_sql)
    con.commit()
    if cursor.rowcount == 1:
        con.close()
        return True
    else:
        con.close()
        return False