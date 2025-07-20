from sqlalchemy.orm import Session
import models, schemas, auth

def create_user(db: Session, user: schemas.UserCreate):
    hashed = auth.hash_password(user.password)
    db_user = models.User(name=user.name, email=user.email, password=hashed, role=user.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, email: str, password: str):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user or not auth.verify_password(password, user.password):
        return None
    return user

def create_assignment(db: Session, assignment: schemas.AssignmentCreate, teacher_id: int):
    db_assignment = models.Assignment(**assignment.dict(), teacher_id=teacher_id)
    db.add(db_assignment)
    db.commit()
    db.refresh(db_assignment)
    return db_assignment

def submit_assignment(db: Session, assignment_id: int, student_id: int, content: str):
    submission = models.Submission(
        assignment_id=assignment_id,
        user_id=student_id,  
        content=content
    )
    db.add(submission)
    db.commit()
    db.refresh(submission)
    return submission

def get_submissions(db: Session, assignment_id: int):
    return db.query(models.Submission).filter(models.Submission.assignment_id == assignment_id).all()
