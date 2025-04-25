from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.database.db import Base

class Survey(Base):
    __tablename__ = "surveys"

    id = Column(Integer, primary_key=True, index=True)
    age = Column(Integer)
    gender = Column(String, index=True)
    zip_code = Column(String)
    city = Column(String, index=True)
    state = Column(String, index=True)
    income = Column(String)
    education_level = Column(String, index=True)
    q1_rating = Column(Integer)
    q2_rating = Column(Integer)
    q3_open = Column(Text)
    q4_rating = Column(Integer)
    q5_open = Column(Text)
    sentiment_label = Column(String, index=True) 