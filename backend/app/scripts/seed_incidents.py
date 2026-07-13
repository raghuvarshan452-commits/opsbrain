from datetime import datetime
 
from app.db.postgres import SessionLocal
from app.models.orm_models import Equipment, Incident
 
SAMPLE_EQUIPMENT = [
    {"tag_number": "P-204", "equipment_class": "Centrifugal Pump", "location": "Unit 3"},
    {"tag_number": "C-101", "equipment_class": "Compressor", "location": "Unit 1"},
    {"tag_number": "V-305", "equipment_class": "Pressure Vessel", "location": "Unit 5"},
]
 
SAMPLE_INCIDENTS = [
    {"tag": "P-204", "description": "Hydraulic seal failure caused unexpected shutdown.", "date": datetime(2025, 3, 12), "severity": "high"},
    {"tag": "P-204", "description": "Vibration levels exceeded threshold during routine inspection.", "date": datetime(2025, 6, 2), "severity": "medium"},
    {"tag": "P-204", "description": "Seal replacement performed after minor leak detected.", "date": datetime(2025, 9, 18), "severity": "low"},
    {"tag": "C-101", "description": "Compressor tripped due to high discharge temperature.", "date": datetime(2025, 4, 22), "severity": "high"},
    {"tag": "C-101", "description": "Lubrication system flagged low oil pressure warning.", "date": datetime(2025, 7, 30), "severity": "medium"},
    {"tag": "V-305", "description": "Pressure relief valve activated during process upset.", "date": datetime(2025, 5, 15), "severity": "high"},
]
 
 
def seed():
    db = SessionLocal()
 
    if db.query(Equipment).count() == 0:
        for e in SAMPLE_EQUIPMENT:
            db.add(Equipment(**e))
        db.commit()
        print(f"Seeded {len(SAMPLE_EQUIPMENT)} equipment records.")
    else:
        print("Equipment table already populated — skipping.")
 
    if db.query(Incident).count() == 0:
        equipment_map = {e.tag_number: e.id for e in db.query(Equipment).all()}
        for inc in SAMPLE_INCIDENTS:
            db.add(
                Incident(
                    equipment_id=equipment_map[inc["tag"]],
                    description=inc["description"],
                    incident_date=inc["date"],
                    severity=inc["severity"],
                )
            )
        db.commit()
        print(f"Seeded {len(SAMPLE_INCIDENTS)} incident records.")
    else:
        print("Incident table already populated — skipping.")
 
    db.close()
 
 
if __name__ == "__main__":
    seed()
