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
    return {"total": total, "items": surveys}

@router.get("/surveys/{survey_name}", response_model=List[SurveySchema])
def get_survey_by_name(
    survey_name: str,
    db: Session = Depends(get_db)
):
    """
    Get surveys filtered by survey name
    Note: In this implementation, we only have one survey, 
    but this would allow filtering by survey name in a real-world scenario
    """
    # Since we only have one survey in this example, we'll just return all surveys
    surveys = db.query(Survey).all()
    if not surveys:
        raise HTTPException(status_code=404, detail="No surveys found")
    return surveys 