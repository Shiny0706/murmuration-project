from pydantic import BaseModel
from typing import Optional, List

class SurveyBase(BaseModel):
    age: int
    gender: str
    zip_code: str
    city: str
    state: str
    income: str
    education_level: str
    q1_rating: int
    q2_rating: int
    q3_open: str
    q4_rating: int
    q5_open: str
    sentiment_label: str
    is_human: bool

class SurveyCreate(SurveyBase):
    pass

class Survey(SurveyBase):
    id: int

    class Config:
        from_attributes = True

class QuestionResponse(BaseModel):
    id: int
    age: int
    gender: str
    education_level: str
    response: str  # This will either be the rating or the open-ended response
    sentiment_label: Optional[str] = None

    class Config:
        from_attributes = True 