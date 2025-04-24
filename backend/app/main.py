from fastapi import FastAPI, Depends, UploadFile, File
from sqlalchemy.orm import Session
import pandas as pd
from . import models, schemas, crud
from .database import engine, SessionLocal
import io

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/surveys")
def read_all(db: Session = Depends(get_db)):
    return crud.get_all_responses(db)

@app.get("/surveys/{survey_name}")
def read_by_survey(survey_name: str, db: Session = Depends(get_db)):
    return crud.get_by_survey(db, survey_name)

@app.get("/questions/{question_id}")
def read_by_question(question_id: str, db: Session = Depends(get_db)):
    return crud.get_by_question(db, question_id)

@app.post("/upload")
async def upload_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    contents = await file.read()
    df = pd.read_csv(io.BytesIO(contents))
    for _, row in df.iterrows():
        data = schemas.SurveyResponseCreate(
            age=row["age"],
            gender=row["gender"],
            zip_code=str(row["zip_code"]),
            city=row["city"],
            state=row["state"],
            income=row["income"],
            education_level=row["education_level"],
            q1_rating=row["q1_rating"],
            q2_rating=row["q2_rating"],
            q3_open=row["q3_open"],
            q4_rating=row["q4_rating"],
            q5_open=row["q5_open"],
            sentiment_label=row["sentiment_label"]
        )
        crud.create_response(db, data)
    return {"message": "Survey data uploaded successfully"}
