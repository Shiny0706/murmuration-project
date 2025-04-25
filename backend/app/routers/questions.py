from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
from sqlalchemy import func, case, distinct

from app.database.db import get_db
from app.models.survey import Survey
from app.models.schemas import QuestionResponse

router = APIRouter()

@router.get("/questions/{question_id}", response_model=List[Dict[str, Any]])
def get_question_responses(
    question_id: str,
    group_by: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Get responses for a specific question
    Optionally group by demographic factors (gender, education_level, sentiment_label)
    """
    valid_questions = ["q1_rating", "q2_rating", "q3_open", "q4_rating", "q5_open"]
    valid_group_by = ["gender", "education_level", "sentiment_label", "age", None]
    
    if question_id not in valid_questions:
        raise HTTPException(status_code=400, detail=f"Invalid question ID. Must be one of {valid_questions}")
    
    if group_by and group_by not in valid_group_by:
        raise HTTPException(status_code=400, detail=f"Invalid group_by parameter. Must be one of {valid_group_by}")
    
    # For numeric rating questions
    if question_id in ["q1_rating", "q2_rating", "q4_rating"]:
        if group_by:
            # Group responses by the specified demographic
            query = db.query(
                getattr(Survey, group_by),
                func.avg(getattr(Survey, question_id)).label("average"),
                func.count(getattr(Survey, question_id)).label("count")
            ).group_by(getattr(Survey, group_by))
            
            results = query.all()
            return [{"group": getattr(r, group_by), "average": float(r.average), "count": r.count} for r in results]
        else:
            # Overall statistics
            result = db.query(
                func.avg(getattr(Survey, question_id)).label("average"),
                func.min(getattr(Survey, question_id)).label("min"),
                func.max(getattr(Survey, question_id)).label("max"),
                func.count(getattr(Survey, question_id)).label("count")
            ).first()
            
            # Calculate distribution (count of each rating value)
            distribution = {}
            for i in range(1, 6):  # Ratings 1-5
                count = db.query(func.count(getattr(Survey, question_id))).filter(
                    getattr(Survey, question_id) == i
                ).scalar()
                distribution[str(i)] = count
            
            return [{
                "average": float(result.average),
                "min": result.min,
                "max": result.max,
                "count": result.count,
                "distribution": distribution
            }]
    
    # For open-ended questions
    else:
        if group_by:
            # Get unique responses and counts, grouped by demographic
            results = db.query(
                getattr(Survey, group_by),
                getattr(Survey, question_id),
                func.count(getattr(Survey, question_id)).label("count")
            ).group_by(
                getattr(Survey, group_by), 
                getattr(Survey, question_id)
            ).all()
            
            # Organize by group
            grouped_data = {}
            for r in results:
                group = getattr(r, group_by)
                if group not in grouped_data:
                    grouped_data[group] = []
                grouped_data[group].append({
                    "response": getattr(r, question_id),
                    "count": r.count
                })
            
            return [{"group": group, "responses": responses} for group, responses in grouped_data.items()]
        else:
            # Get all unique responses with counts
            results = db.query(
                getattr(Survey, question_id),
                func.count(getattr(Survey, question_id)).label("count")
            ).group_by(getattr(Survey, question_id)).all()
            
            responses = [{"response": getattr(r, question_id), "count": r.count} for r in results]
            return [{"responses": responses}] 