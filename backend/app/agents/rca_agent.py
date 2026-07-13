"""
Maintenance / RCA Agent
------------------------
Inputs:   Equipment tag (e.g. "P-204")
Outputs:  Ranked root-cause hypotheses with supporting evidence
Memory:   Reads incident history from Postgres
Talks to: Knowledge Graph Agent, Lessons-Learned Agent (later phase)
"""
import json
import re

from groq import Groq

from app.core.config import settings
from app.db.postgres import SessionLocal
from app.models.orm_models import Equipment, Incident

client = Groq(api_key=settings.llm_api_key)

RCA_PROMPT = """You are an industrial Root Cause Analysis assistant.
Given the equipment's incident history below, propose the most likely root
causes, ranked from most to least likely.

Return ONLY a JSON array, no markdown fences, no preamble, no explanation
outside the array. Each item must have:
- "hypothesis": a short root-cause description
- "confidence": a number from 0.0 to 1.0
- "supporting_evidence": a short string citing which incident(s) support this

Incident history for equipment {tag}:
{incident_text}
"""


def _extract_json_array(raw: str) -> str:
    """Pull out the first [...] JSON array from a string, in case the model
    wrapped it in stray prose despite instructions not to."""
    match = re.search(r"\[.*\]", raw, re.DOTALL)
    return match.group(0) if match else raw


class RCAAgent:
    def analyze(self, equipment_tag: str) -> dict:
        db = SessionLocal()
        equipment = db.query(Equipment).filter(Equipment.tag_number == equipment_tag).first()

        if not equipment:
            db.close()
            return {"equipment_tag": equipment_tag, "hypotheses": [], "note": "No equipment record found."}

        incidents = db.query(Incident).filter(Incident.equipment_id == equipment.id).all()
        db.close()

        if not incidents:
            return {
                "equipment_tag": equipment_tag,
                "hypotheses": [],
                "note": "No incident history found for this equipment.",
            }

        incident_text = "\n".join(
            f"- [{i.incident_date}] ({i.severity}): {i.description}" for i in incidents
        )
        prompt = RCA_PROMPT.format(tag=equipment_tag, incident_text=incident_text)

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}],
        )

        raw = response.choices[0].message.content.strip()
        raw = raw.removeprefix("```json").removeprefix("```").removesuffix("```").strip()

        try:
            hypotheses = json.loads(raw)
        except json.JSONDecodeError:
            try:
                hypotheses = json.loads(_extract_json_array(raw))
            except json.JSONDecodeError:
                print("RAW GROQ RESPONSE (unparseable):", repr(raw))
                hypotheses = []

        return {"equipment_tag": equipment_tag, "hypotheses": hypotheses, "incident_count": len(incidents)}