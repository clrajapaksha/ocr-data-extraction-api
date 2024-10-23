import os

import uvicorn

from typing import List
from typing_extensions import Annotated

from fastapi import Depends, FastAPI, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security.api_key import APIKey
import auth

from middleware.validate_middleware import ValidateUploadFileSizeMiddleware

import storage

#from sqlalchemy.orm import Session

#from . import crud, models, schemas
# from .database import SessionLocal, engine

#models.Base.metadata.create_all(bind=engine)

description = """
OCR Data Extraction API helps you to find answers from relevant documents. 🚀

## Documents

You will be able to:

* **Upload documents**.
* **Get text from documents using OCR** (_mocked_).

## Extract Data

You can **extract data** from documents using a natural language query.

"""

app = FastAPI(
    title="OCR Data Extraction API",
    description=description,
    summary="Question answering from OCRed documents",
    version="0.0.1",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Chathuranga Rajapaksha",
        "url": "https://www.linkedin.com/in/clrajapaksha/",
        "email": "clrajapaksha@gmail.com",
    },
)

app.add_middleware(
    ValidateUploadFileSizeMiddleware,
    max_content_size=5*1024*1024  # 5MB
)

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

APIKeyDependency = Annotated[APIKey, Depends(auth.get_api_key)]

@app.post("/upload", tags=["Documents"])
async def upload_file(files: List[UploadFile], api_key: APIKeyDependency):
    for file in files:
        if file.content_type not in ["application/pdf", "image/tiff", "image/jpeg", "image/png"]:
            raise HTTPException(400, detail="Invalid document type")
    return await storage.upload_file_to_storage(files, "pdf")

    # return {"filenames": [file.filename for file in files]}


@app.post("/ocr", tags=["Documents"])
async def ocr():
    await storage.download_file_from_storage("")
    return "OCR completed"


@app.post("/extract", tags=["Extract Data"])
def extract():
    return "extracted"


port = int(os.environ["PORT"])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=port)
