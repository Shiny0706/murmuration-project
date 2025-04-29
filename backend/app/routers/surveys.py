from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel, Field, validator
from datetime import datetime


from app.database.db import get_db
from app.models.survey import Survey
from app.models.schemas import Survey as SurveySchema

router = APIRouter()


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

@router.get("/surveys", response_model=PaginatedResponse)
def get_all_surveys(
    cursor: Optional[str] = None,
    page_size: int = Query(default=50, ge=1, le=100),
    db: Session = Depends(get_db)
):
    # Decode cursor if provided
    last_id = decode_cursor(cursor) if cursor else 0
    
    # Query with cursor-based pagination
    query = db.query(Survey)
    if last_id:
        query = query.filter(Survey.id > last_id)
    
    # Get one extra item to determine if there are more pages
    items = query.order_by(Survey.id).limit(page_size + 1).all()
    
    has_more = len(items) > page_size
    items = items[:page_size]  # Remove the extra item
    
    # Generate next cursor
    next_cursor = encode_cursor(items[-1].id) if has_more else None
    
    return {
        "items": items,
        "total": db.query(Survey.id).count(),
        "next_cursor": next_cursor,
        "page_size": page_size,
        "has_more": has_more
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