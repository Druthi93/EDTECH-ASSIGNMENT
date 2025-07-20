from pydantic import BaseModel, EmailStr
from typing import Optional
import datetime
from enum import Enum

class UserRole(str, Enum):
    student = "student"
    teacher = "teacher"

class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    role: UserRole

class UserLogin(BaseModel):
    email: EmailStr
    password: str

from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str
    role: str


class AssignmentCreate(BaseModel):
    title: str
    description: str
    due_date: datetime.datetime

class AssignmentOut(BaseModel):
    id: int
    title: str
    description: str
    due_date: datetime.datetime
    class Config:
        orm_mode = True

class SubmissionCreate(BaseModel):
    title: str
    content: str

class SubmissionOut(BaseModel):
    id: int
    content: str
    submitted_at: datetime.datetime
    student_id: int
    class Config:
        orm_mode = True

class SubmissionOut(BaseModel):
    assignment_id: int
    submitted_by: str
    content: str

    class Config:
        orm_mode = True
