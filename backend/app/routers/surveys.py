from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel, Field, validator
from datetime import datetime
import base64

from app.database.db import get_db
from app.models.survey import Survey
from app.models.schemas import Survey as SurveySchema

router = APIRouter()

def encode_cursor(last_id: int) -> str:
    return base64.urlsafe_b64encode(str(last_id).encode()).decode()

def decode_cursor(cursor: str) -> int:
    return int(base64.urlsafe_b64decode(cursor.encode()).decode())

class SurveyListResponse(BaseModel):
    total: int
    items: List[SurveySchema]

class PaginatedResponse(BaseModel):
    items: List[SurveySchema]
    total: int
    next_cursor: Optional[str]
    page_size: int
    has_more: bool

class SurveyBase(BaseModel):
    age: int = Field(ge=0, le=120)
    gender: str = Field(max_length=50)
    zip_code: str = Field(pattern=r"^\d{5}(-\d{4})?$")
    city: str = Field(max_length=100)
    state: str = Field(max_length=2)
    income: str = Field(max_length=50)
    education_level: str = Field(max_length=50)
    q1_rating: int = Field(ge=1, le=5)
    q2_rating: int = Field(ge=1, le=5)
    q3_open: str = Field(max_length=1000)
    q4_rating: int = Field(ge=1, le=5)
    q5_open: str = Field(max_length=1000)
    sentiment_label: str = Field(pattern=r"^(Positive|Negative|Neutral)$")

    @validator('state')
    def validate_state(cls, v):
        valid_states = ['AL', 'AK', 'AZ', ...]  # All US state codes
        if v.upper() not in valid_states:
            raise ValueError('Invalid state code')
        return v.upper()

class PaginatedSurveyResponse(BaseModel):
    items: List[SurveySchema]
    total: int
    next_cursor: Optional[str]
    page_size: int
    has_more: bool
    sentiment_counts: dict

@router.get("/surveys", response_model=PaginatedSurveyResponse)
def get_all_surveys(
    cursor: Optional[str] = None,
    page_size: int = Query(50, ge=1, le=100),
    gender: Optional[str] = None,
    education_level: Optional[str] = None,
    state: Optional[str] = None,
    city: Optional[str] = None,
    sentiment: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Get all survey responses with optional filtering and cursor-based pagination.
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

    # Cursor-based pagination
    if cursor:
        last_id = decode_cursor(cursor)
        query = query.filter(Survey.id > last_id)
    query = query.order_by(Survey.id)

    # Get one extra item to check if there is a next page
    items = query.limit(page_size + 1).all()
    has_more = len(items) > page_size
    items = items[:page_size]

    # Prepare next cursor
    next_cursor = encode_cursor(items[-1].id) if has_more and items else None

    # Sentiment analysis for the filtered result set
    sentiment_counts = {"Positive": 0, "Negative": 0, "Neutral": 0}
    for survey in items:
        if survey.sentiment_label in sentiment_counts:
            sentiment_counts[survey.sentiment_label] += 1

    total = db.query(Survey).count()

    return {
        "items": items,
        "total": total,
        "next_cursor": next_cursor,
        "page_size": page_size,
        "has_more": has_more,
        "sentiment_counts": sentiment_counts
    }

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