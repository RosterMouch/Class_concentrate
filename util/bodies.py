from pydantic import BaseModel
class AuthroizeBody(BaseModel):
    student_id: int
    student_pwd: str
class courseQueryBody(BaseModel):
    student_id: int