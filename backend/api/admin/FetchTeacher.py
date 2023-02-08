#Author:Elin 
#Create Time:2023-02-07 23:17:39
#Last Modified By:Elin
#Update Time:2023-02-07 23:17:39
import pymysql as sql
import json
config = json.load(open('../config/db.json', 'r'))
ip = config['server']['ip']
db = config['database']['db']
user = config['database']['user']
password = config['database']['pwd']
charset = config['database']['charset']

def fetchTeacher():
    con = sql.connect(host=ip, user=user, password=password, db=db, charset=charset)
    cursor = con.cursor()
    excute_sql = f"""
    SELECT * FROM TEACHER;
    """
    cursor.execute(excute_sql)

    result = cursor.fetchall()
    response = []
    for i in range(len(result)):
        respBody = {
            "teacher_id": result[i][0],
            "teacher_name": result[i][1],
            "teacher_password": result[i][2],
        }
        response.append(respBody)
    con.close()
    return response