#Author: Elin
#Date: 2023-01-24 12:35:51
 #Last Modified by:   Elin 
 #Last Modified time: 2023-01-24 12:35:51 
import pymysql as sql
from hashlib import md5
import json
import pandas as pd

config = json.load(open('../config/db.json', 'r'))
ip = config['server']['ip']
db = config['database']['db']
user = config['database']['user']
password = config['database']['pwd']
charset = config['database']['charset']

def allRank(teacher_id):
    con = sql.connect(host=ip, user=user, password=password, db=db, charset=charset)
    con.autocommit(True)
    courseList = f"select course_id,course_name from course where teacher_id = {teacher_id};"
    course_df = pd.read_sql(courseList,con)
    course_id = course_df['course_id'].tolist()
    course_name = course_df['course_name'].tolist()
    replay_sql = f"select course_id,student_status from replay where course_id in {tuple(course_id)};"
    replay_df = pd.read_sql(replay_sql,con)
    replay_df = replay_df.groupby('course_id').count().sort_values(by=['student_status'],ascending=False)
    allindex = [ i for i in replay_df.index.tolist()]
    allvalues = [i for i in replay_df.values.tolist()[0]]
    allname = [ course_name[course_id.index(i)] for i in allindex]
    allpercent = [ round(i/replay_df.shape[0],2) * 100 for i in allvalues]
    resp = {
        "course_id":allindex,
        "course_name":allname,
        "concentrated":allvalues,
        "percent":allpercent
    }
    con.close()
    return resp