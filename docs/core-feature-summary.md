# OpsBrain — Core Feature Summary

## Agents (9 total — Orchestrator + 8 specialized)

1. **Orchestrator Agent** — LangGraph-based routing, returns a step-by-step trace (Day 7)
2. **Document Ingestion Agent** — routes files to OCR or direct text extraction (Day 3)
3. **OCR Agent** — Tesseract-based, handles scanned PDFs and images (Day 3)
4. **Entity Extraction Agent** — Groq (Llama 3.3-70b)-based structured extraction: equipment tags, dates, personnel, standards (Day 4)
5. **Knowledge Graph Agent** — Neo4j writes, normalization/dedup, cross-reference tracking, LLM-based contradiction detection (Day 4, 5, 13)
6. **Expert Copilot Agent** — RAG retrieval via ChromaDB, cited answers, hallucination guardrail, robust JSON parsing with regex fallback (Day 6, 8)
7. **Compliance Agent** — regulation gap detection via embedding similarity against 15 seeded OISD/Factory Act/DGMS-style clauses (Day 9)
8. **RCA Agent** — ranked root-cause hypotheses from seeded incident history, Groq-based (Day 10)
9. **Lessons-Learned Agent** — proactive alerts from cross-referenced entities + incident history, no new data required (Day 11)

## API Endpoints

- `GET /api/health`, `GET /api/db-health`
- `POST /api/documents/upload`, `GET /api/documents`
- `GET /api/graph`, `POST /api/graph/detect-contradictions`
- `POST /api/copilot/query`
- `POST /api/compliance/check/{document_id}`
- `GET /api/rca/{equipment_tag}`
- `GET /api/alerts`
- `GET /api/analytics/summary`, `GET /api/analytics/roi`, `GET /api/audit-log`

## Screens (10 total)

Login, Dashboard, Upload, Copilot, Knowledge Graph Explorer, Compliance,
Maintenance, Notifications, Analytics, Settings

## Known Scope Decisions (intentional, not bugs)

- Alerts are computed on-demand, not persisted (Day 11) — dismiss is client-side only
- Document upload flow is NOT routed through the Orchestrator (Day 7) — only the
  Copilot query path is, since that's the visible interaction judges see
- Chunking is fixed-size with overlap, not semantic/paragraph-aware (Day 5)
- Compliance thresholds (covered/partial/missing cutoffs) were tuned by observing
  real embedding distance spreads against test documents, not formally validated
  against a large labeled dataset
- All LLM-based agents (Copilot, RCA, Contradiction Detector) use Groq's
  Llama 3.3-70b-versatile, chosen for speed and cost during development
- Regulation corpus (15 clauses) and equipment/incident data (3 equipment, 6
  incidents) are illustrative seed data, not a real regulatory database

