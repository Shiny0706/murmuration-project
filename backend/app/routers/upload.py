from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
import pandas as pd
import io
#when I want to use OpenAi for detect the human written survey start
# import openai
# import os
# openai.api_key = os.getenv("OPENAI_API_KEY")
#when I want to use OpenAi for detect the human written survey end

from app.database.db import get_db
from app.models.survey import Survey

router = APIRouter()

#when I want to use OpenAi for detect the human written survey start
# async def detect_human_openai(text: str) -> bool:
#     if not text or len(text) < 10:
#         return False
#     prompt = f"Decided whether this survey response was written by a human or an AI. Reply with only 'human' or 'ai'.\n\n{text}"
#     response = await openai.Completion.create(
#         model="gpt-3.5-turbo",
#         messages=[{"role": "user", "content": prompt}],
#         temperature=0.0,
#         max_tokens=5,
#     )
#     return response.choices[0].text.strip().lower() == "human"
#when I want to use OpenAi for detect the human written survey end


def detect_human(text: str) -> bool:
    """
    Detect if the text is human-generated or AI-generated
    """
    if not text or len(text) < 20:
        return False # Very short text likely AI
    suspicious_phrases = ["as an AI", "as an assistant", "as a language model", "as a chatbot", "as a virtual assistant", "as a virtual agent", "as a virtual assistant", "as a virtual agent", "as a virtual assistant", "as a virtual agent", "I'm an AI", "I'm an assistant", "I'm a language model", "I'm a chatbot", "I'm a virtual assistant", "I'm a virtual agent", "I'm a virtual assistant", "I'm a virtual agent", "I'm a virtual assistant", "I'm a virtual agent", "AI will"]
    if any(phrase.lower() in text.lower() for phrase in suspicious_phrases):
        return False
    if text.count(".") > 5: # Too formal/long sentences
        return False
    return True

@router.post("/upload")
async def upload_csv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Upload a CSV file with survey data
    """
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are supported")
    
    try:
        # Read CSV file
        contents = await file.read()
        df = pd.read_csv(io.StringIO(contents.decode('utf-8')))
        
        # Clean up existing data (optional - depends on requirements)
        db.query(Survey).delete()
        
        # Convert DataFrame to list of dictionaries
        survey_data = df.to_dict(orient='records')
        
        # Insert new data
        for data in survey_data:
            # Create Survey object
            survey = Survey(
                id=data.get('id'),
                age=data.get('age'),
                gender=data.get('gender'),
                zip_code=data.get('zip_code'),
                city=data.get('city'),
                state=data.get('state'),
                income=data.get('income'),
                education_level=data.get('education_level'),
                q1_rating=data.get('q1_rating'),
                q2_rating=data.get('q2_rating'),
                q3_open=data.get('q3_open'),
                q4_rating=data.get('q4_rating'),
                q5_open=data.get('q5_open'),
                sentiment_label=data.get('sentiment_label'),
                is_human=detect_human(data.get('q5_open') or data.get('q3_open'))
            )
            db.add(survey)
        
        db.commit()
        surveys = db.query(Survey).all()
        sentiment_counts = {"Positive": 0, "Negative": 0, "Neutral": 0}
        for survey in surveys:
            if survey.sentiment_label in sentiment_counts:
                sentiment_counts[survey.sentiment_label] += 1
        return {"detail": f"Successfully uploaded {len(survey_data)} survey records", "surveys": surveys, "sentiment_counts": sentiment_counts}
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to process CSV file: {str(e)}")
    finally:
        await file.close() 