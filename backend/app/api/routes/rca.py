from fastapi import APIRouter
 
from app.agents.rca_agent import RCAAgent
 
router = APIRouter()
rca_agent = RCAAgent()
 
 
@router.get("/rca/{equipment_tag}")
def get_rca(equipment_tag: str):
    return rca_agent.analyze(equipment_tag)

