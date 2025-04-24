from sqlalchemy.orm import Session
from . import models, schemas

def create_response(db: Session, data: schemas.SurveyResponseCreate):
    response = models.SurveyResponse(**data.dict())
    db.add(response)
    db.commit()
    db.refresh(response)
    return response

def get_all_responses(db: Session):
    return db.query(models.SurveyResponse).all()

def get_by_survey(db: Session, survey_name: str):
    return db.query(models.SurveyResponse).filter(models.SurveyResponse.survey_name == survey_name).all()

def get_by_question(db: Session, question_id: str):
    return db.query(models.SurveyResponse).filter(models.SurveyResponse.question_id == question_id).all()
