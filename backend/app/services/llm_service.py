import json
from groq import Groq
from app.core.config import settings

client = Groq(api_key=settings.llm_api_key)

EXTRACTION_PROMPT = """You are an industrial document entity extractor.
Extract entities from the text below. Return ONLY a JSON array, no other text,
no markdown code fences.
Each item must have exactly these keys:
- "entity_type": one of "equipment_tag", "date", "personnel", "standard_reference"
- "value": the exact extracted string
- "confidence": a number from 0.0 to 1.0

Text:
{text}
"""

def extract_entities(text: str) -> list[dict]:
    prompt = EXTRACTION_PROMPT.format(text=text[:6000])
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )
    raw = response.choices[0].message.content.strip()
    raw = raw.removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return []