from app.db.postgres import SessionLocal
from app.models.orm_models import Regulation
 
SAMPLE_REGULATIONS = [
    {"clause_ref": "OISD-STD-105 Cl. 4.2", "standard": "OISD", "clause_text": "Permit-to-work must be issued before any hot work is performed near hazardous storage areas."},
    {"clause_ref": "OISD-STD-105 Cl. 5.1", "standard": "OISD", "clause_text": "Gas testing must be conducted and documented prior to confined space entry."},
    {"clause_ref": "Factory Act Sec. 87", "standard": "Factory Act", "clause_text": "Dangerous machinery must be fitted with adequate safety guards to prevent operator injury."},
    {"clause_ref": "Factory Act Sec. 92", "standard": "Factory Act", "clause_text": "Records of all workplace accidents must be maintained and reported to the Chief Inspector."},
    {"clause_ref": "DGMS Circular 12/2019", "standard": "DGMS", "clause_text": "Mine ventilation systems require quarterly inspection and documented maintenance logs."},
    {"clause_ref": "DGMS Circular 07/2021", "standard": "DGMS", "clause_text": "Personal protective equipment must be issued and its usage verified for all underground personnel."},
    {"clause_ref": "OISD-STD-118 Cl. 3.4", "standard": "OISD", "clause_text": "Pressure relief valves must undergo calibration testing at least once every 12 months."},
    {"clause_ref": "OISD-STD-118 Cl. 6.2", "standard": "OISD", "clause_text": "Emergency shutdown systems must be tested and results logged on a monthly basis."},
    {"clause_ref": "Factory Act Sec. 45", "standard": "Factory Act", "clause_text": "Adequate fire-fighting equipment must be provided, tested, and readily accessible in all sections."},
    {"clause_ref": "Factory Act Sec. 112", "standard": "Factory Act", "clause_text": "Workers must receive documented safety training before being assigned to hazardous processes."},
    {"clause_ref": "DGMS Circular 03/2020", "standard": "DGMS", "clause_text": "All lifting equipment must be certified and re-inspected annually by a competent authority."},
    {"clause_ref": "OISD-STD-130 Cl. 2.1", "standard": "OISD", "clause_text": "Storage tanks handling flammable liquids require a documented inspection schedule."},
    {"clause_ref": "OISD-STD-130 Cl. 4.5", "standard": "OISD", "clause_text": "Static electricity grounding must be verified for all flammable liquid transfer operations."},
    {"clause_ref": "Factory Act Sec. 21", "standard": "Factory Act", "clause_text": "Adequate ventilation and temperature control must be maintained in all enclosed work areas."},
    {"clause_ref": "DGMS Circular 15/2018", "standard": "DGMS", "clause_text": "Any equipment failure resulting in a near-miss must be documented and reviewed within 48 hours."},
]
 
 
def seed():
    db = SessionLocal()
    existing = db.query(Regulation).count()
    if existing > 0:
        print(f"Regulations table already has {existing} rows — skipping seed.")
        db.close()
        return
 
    for r in SAMPLE_REGULATIONS:
        db.add(Regulation(clause_ref=r["clause_ref"], standard=r["standard"], clause_text=r["clause_text"]))
    db.commit()
    print(f"Seeded {len(SAMPLE_REGULATIONS)} regulation clauses.")
    db.close()
 
 
if __name__ == "__main__":
    seed()
