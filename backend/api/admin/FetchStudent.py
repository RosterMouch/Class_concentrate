#Author:Elin 
#Create Time:2023-02-08 00:11:55
#Last Modified By:Elin
#Update Time:2023-02-08 00:11:55
  
import pymysql as sql
import json
config = json.load(open('../config/db.json', 'r'))
ip = config['server']['ip']
db = config['database']['db']
user = config['database']['user']
password = config['database']['pwd']
charset = config['database']['charset']

def fetchStudent():
    con = sql.connect(host=ip, user=user, password=password, db=db, charset=charset)
    cursor = con.cursor()
    excute_sql = f"""
    SELECT * FROM STUDENT;
    """
    cursor.execute(excute_sql)

    result = cursor.fetchall()
    response = []
    for i in range(len(result)):
        respBody = {
            "student_id": result[i][0],
            "student_name": result[i][1],
            "student_class": result[i][2],
            "student_grade": result[i][3],
            "student_major": result[i][4],
            "student_password": result[i][5],
        }
        response.append(respBody)
    con.close()
    return response