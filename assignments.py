from fastapi import APIRouter, Depends, HTTPException, status
from database import SessionLocal
import schemas, crud, models, auth
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer

router = APIRouter(prefix="/assignments", tags=["Assignments"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = auth.decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    return payload

@router.post("/", response_model=schemas.AssignmentOut)
def create_assignment(assignment: schemas.AssignmentCreate,
                      db: Session = Depends(get_db),
                      user=Depends(get_current_user)):
    if user["role"] != "teacher":
        raise HTTPException(status_code=403, detail="Only teachers can create assignments")
    return crud.create_assignment(db, assignment, teacher_id=int(user["sub"]))
