from pydantic import BaseModel

class SurveyResponseCreate(BaseModel):
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

class SurveyResponseOut(SurveyResponseCreate):
    id: int
    class Config:
        orm_mode = True
