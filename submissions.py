from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer

from database import SessionLocal
import schemas, crud, auth
import models

router = APIRouter(prefix="/submissions", tags=["Submissions"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = auth.decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    return payload

@router.post("/submissions/")
def submit_assignment(sub: schemas.SubmissionCreate,
                      db: Session = Depends(get_db),
                      current_user: models.User = Depends(get_current_user)):
    db_sub = models.Submission(
        title=sub.title,
        content=sub.content,
        user_id=current_user.id
    )
    db.add(db_sub)
    db.commit()
    db.refresh(db_sub)
    return {"message": "Submission successful", "id": db_sub.id}


@router.get("/assignments/{assignment_id}/submissions/")
def get_submissions_by_assignment_id(
    assignment_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    if current_user["role"] != "teacher":
        raise HTTPException(status_code=403, detail="Only teachers can view submissions")
    
    submissions = db.query(models.Submission).filter_by(assignment_id=assignment_id).all()

    if not submissions:
        return {"message": "No submissions found"}

    result = []
    for s in submissions:
        student = db.query(models.User).filter_by(id=s.user_id).first()
        result.append({
            "assignment_id": s.assignment_id,
            "submitted_by": student.email if student else "Unknown",
            "content": s.content
        })

    return result
