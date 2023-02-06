#Author:Elin 
#Create Time:2023-02-02 17:39:39
#Last Modified By:Elin
#Update Time:2023-02-02 17:39:39
from fastapi import FastAPI,status,UploadFile
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from hashlib import md5
import os,sys
# 设置跨目录导入模块
current_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(current_path)
from util.bodies import AuthroizeBody,courseQueryBody
from api.AuthCheck import auth_Check
from api.CourseQuerying import courseQuerying
origins = [
    "http://127.0.0.1:1430",
    "http://127.0.0.1"
    "http://localhost",
    "http://localhost:8080"
]
app = FastAPI(
    title="接口文档",
    description="学生端API结构文档查询",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials = True,
    allow_methods=['*'],
    allow_headers=['*']
)

@app.post("/v1/student/login")
async def login(body:AuthroizeBody):
    student_id = body.student_id
    student_pwd = body.student_pwd
    try:
        result = auth_Check(
            student_id= student_id,
            student_pwd=student_pwd
        )
        return {
            'code':status.HTTP_200_OK,
            'data':result[0:4]
        }
    except Exception as e:
        return {
            'code':status.HTTP_500_INTERNAL_SERVER_ERROR,
            'message':str(e),
            "atFile":e.__traceback__.tb_frame.f_globals["__file__"],
            "atLine":e.__traceback__.tb_lineno
        }
@app.post("/v1/student/checkcourse")
async def checkcourse(body:courseQueryBody):
    st_id = body.student_id
    try:
        result = courseQuerying(student_id=st_id)
        return {
            'code':status.HTTP_200_OK,
            'data':result
        }
    except Exception as e:
        return {
            'code':status.HTTP_500_INTERNAL_SERVER_ERROR,
            'message':str(e)
        }
@app.post("/upload/")
async def upload(file:UploadFile):
    fileByte = file.file.read()
    print(fileByte)
    if fileByte != None:
        return {
            'code':status.HTTP_202_ACCEPTED,
            'message':'upload sucess'
        }
    else:
        return {
            'code':status.HTTP_501_NOT_IMPLEMENTED,
            'message':'upload failed'
        }
if __name__ == "__main__":
    uvicorn.run("server:app",
        host="192.168.174.11",
        port=8080,
        reload=True,
        reload_dirs=[".","../config","../api","../util"],
        debug=True
    )