from fastapi import APIRouter
 
from app.agents.lessons_learned_agent import LessonsLearnedAgent
 
router = APIRouter()
lessons_learned_agent = LessonsLearnedAgent()
 
 
@router.get("/alerts")
def get_alerts():
    return lessons_learned_agent.scan_for_patterns()
