from sqlalchemy import Column, Integer, String, Enum as SQLAEnum, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from database import Base
from enum import Enum
from datetime import datetime

class RoleEnum(str, Enum):
    student = "student"
    teacher = "teacher"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(SQLAEnum(RoleEnum), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class Assignment(Base):
    __tablename__ = "assignments"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    due_date = Column(DateTime, nullable=False)
    teacher_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

class Submission(Base):
    __tablename__ = "submissions"

    id = Column(Integer, primary_key=True, index=True)
    assignment_id = Column(Integer, ForeignKey("assignments.id"))
    user_id = Column(Integer, ForeignKey("users.id")) 
    content = Column(Text, nullable=False)
