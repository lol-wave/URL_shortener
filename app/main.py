from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from . import schemas, crud, auth, database, dependencies
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    database.Base.metadata.create_all(bind=database.engine)
    # Auto-create default user if not exists
    db = next(database.get_db())
    existing = crud.get_user_by_email(db, "test123@example.com")
    if not existing:
        from schemas import UserCreate
        crud.create_user(db, UserCreate(email="test123@example.com", password="securepassword123"))

@app.post("/shorten", response_model=schemas.URLOut)
def shorten_url(
    url: schemas.URLCreate,
    db: Session = Depends(database.get_db),
    current_user: schemas.UserOut = Depends(dependencies.get_current_user)
):
    return crud.create_url(db, url, user_id=current_user.id)

@app.post("/auth/login")
def login(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = crud.get_user_by_email(db, user.email)
    if not db_user or not auth.verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    access_token = auth.create_access_token(data={"sub": db_user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/{short_code}")
async def redirect_url(short_code: str, db: Session = Depends(database.get_db)):
    db_url = crud.get_url_by_short_code(db, short_code)
    if not db_url:
        raise HTTPException(status_code=404, detail="URL not found")

    return RedirectResponse(url=db_url.original_url)

@app.post("/auth/signup")
def signup(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = crud.create_user(db, user)
    return {"message": "User created successfully", "user": db_user}
