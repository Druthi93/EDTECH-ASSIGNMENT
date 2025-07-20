from fastapi import APIRouter, Depends, HTTPException
import schemas, crud, auth
from sqlalchemy.orm import Session
from database import SessionLocal
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter() 



def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()
from sqlalchemy.exc import IntegrityError

@router.post("/signup")
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        db_user = crud.create_user(db, user)
        token = auth.create_token({"sub": str(db_user.id), "role": db_user.role.value})
        return {
            "access_token": token,
            "token_type": "bearer",
            "role": db_user.role.value
        }
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email already registered")
    except Exception as e:
        db.rollback()
        print("Signup error:", str(e))  
        raise HTTPException(status_code=500, detail="Signup failed: " + str(e))

@router.post("/login")
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.authenticate_user(db, form.username, form.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = auth.create_token({"sub": str(user.id), "role": user.role})

    return {
        "access_token": token,
        "token_type": "bearer",
        "role": user.role.value  
    }

