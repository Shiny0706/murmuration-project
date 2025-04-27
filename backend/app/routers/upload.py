from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
import pandas as pd
import io

from app.database.db import get_db
from app.models.survey import Survey

router = APIRouter()

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
                sentiment_label=data.get('sentiment_label')
            )
            db.add(survey)
        
        db.commit()
        surveys = db.query(Survey).all()
        return {"detail": f"Successfully uploaded {len(survey_data)} survey records", "surveys": surveys}
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to process CSV file: {str(e)}")
    finally:
        await file.close() 