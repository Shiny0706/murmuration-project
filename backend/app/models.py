from sqlalchemy import Column, Integer, String
from .database import Base

class SurveyResponse(Base):
    __tablename__ = "responses"
    id = Column(Integer, primary_key=True, index=True)
    age = Column(Integer)
    gender = Column(String)
    zip_code = Column(String)
    city = Column(String)
    state = Column(String)
    income = Column(String)
    education_level = Column(String)
    q1_rating = Column(Integer)
    q2_rating = Column(Integer)
    q3_open = Column(String)
    q4_rating = Column(Integer)
    q5_open = Column(String)
    sentiment_label = Column(String)
