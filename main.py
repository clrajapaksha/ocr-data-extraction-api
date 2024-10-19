import uvicorn

from typing import List

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
#from sqlalchemy.orm import Session

#from . import crud, models, schemas
# from .database import SessionLocal, engine

#models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# origins = [
#     "http://localhost",
#     "http://localhost:8080",
# ]
#
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


# Dependency
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


# @app.post("/upload")
# def upload_file(user: schemas.UserCreate, db: Session = Depends(get_db)):
#     db_user = crud.get_user_by_email(db, email=user.email)
#     if db_user:
#         raise HTTPException(status_code=400, detail="Email already registered")
#     return crud.create_user(db=db, user=user)


@app.post("/upload")
def upload_file():
    return "uploaded"


@app.post("/ocr")
def ocr():
    return "OCR completed"


@app.post("/extract")
def extract():
    return "extracted"


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
