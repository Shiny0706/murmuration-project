from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel

from app.database.db import get_db
from app.models.survey import Survey
from app.models.schemas import Survey as SurveySchema

router = APIRouter()

class SurveyListResponse(BaseModel):
    total: int
    items: List[SurveySchema]

@router.get("/surveys", response_model=SurveyListResponse)
def get_all_surveys(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=1000),
    gender: Optional[str] = None,
    education_level: Optional[str] = None,
    state: Optional[str] = None,
    city: Optional[str] = None,
    sentiment: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Get all survey responses with optional filtering
    Also return sentiment counts for the filtered result set
    """
    query = db.query(Survey)
    
    # Apply filters if provided
    if gender:
        query = query.filter(Survey.gender == gender)
    if education_level:
        query = query.filter(Survey.education_level == education_level)
    if state:
        query = query.filter(Survey.state == state)
    if city:
        query = query.filter(Survey.city == city)
    if sentiment:
        query = query.filter(Survey.sentiment_label == sentiment)
        
    total = query.count()
    surveys = query.offset(skip).limit(limit).all()

    # Sentiment analysis for the filtered result set
    sentiment_counts = {"Positive": 0, "Negative": 0, "Neutral": 0}
    for survey in surveys:
        if survey.sentiment_label in sentiment_counts:
            sentiment_counts[survey.sentiment_label] += 1
    return {"total": total, "items": surveys, "sentiment_counts": sentiment_counts}

@router.get("/surveys/{survey_name}", response_model=List[SurveySchema])
def get_survey_by_name(
    survey_name: str,
    db: Session = Depends(get_db)
):
    """
    Get surveys filtered by sentiment label (Positive, Negative, Neutral)
    """
    allowed = ["Positive", "Negative", "Neutral"]
    if survey_name not in allowed:
        raise HTTPException(status_code=400, detail="Invalid sentiment label")
    surveys = db.query(Survey).filter(Survey.sentiment_label == survey_name).all()
    if not surveys:
        raise HTTPException(status_code=404, detail="No surveys found")
    return surveys 