"""
Full Pipeline Smoke Test (v2 — expanded for Day 14)
------------------------------------------------------
Run this against a running local backend (uvicorn on port 8000) to verify
the entire pipeline end-to-end, including everything added since Day 8:
Compliance, RCA, Lessons-Learned alerts, Analytics, ROI, and the
Contradiction Detector.
 
Usage:
    python tests/smoke_test.py /path/to/a/test_document.pdf [EQUIPMENT_TAG]
 
Rerun this unchanged on Day 18 for the final pre-freeze regression check.
"""
import sys
import requests
 
BASE_URL = "http://localhost:8000/api"
results = []
 
 
def check(label: str, condition: bool, extra: str = "") -> bool:
    status = "PASS" if condition else "FAIL"
    print(f"[{status}] {label} {extra}")
    results.append(condition)
    return condition
 
 
def run_smoke_test(test_file_path: str, equipment_tag: str = "P-204"):
    # --- Core pipeline (Day 3-8) ---
    r = requests.get(f"{BASE_URL}/health")
    check("GET /health", r.status_code == 200 and r.json().get("status") == "ok")
 
    r = requests.get(f"{BASE_URL}/db-health")
    data = r.json()
    check("Postgres connected", data.get("postgres") == "connected")
    check("Neo4j connected", data.get("neo4j") == "connected")
 
    with open(test_file_path, "rb") as f:
        r = requests.post(f"{BASE_URL}/documents/upload", files={"file": f})
    upload_data = r.json()
    document_id = upload_data.get("document_id")
    check("Document upload", r.status_code == 200 and upload_data.get("status") == "processed")
    check(
        "Entities extracted",
        upload_data.get("entity_count", 0) > 0,
        f"(entity_count={upload_data.get('entity_count')})",
    )
 
    r = requests.get(f"{BASE_URL}/documents")
    check("GET /documents returns list", r.status_code == 200 and len(r.json()) > 0)
 
    r = requests.get(f"{BASE_URL}/graph")
    check("Graph has nodes", len(r.json().get("nodes", [])) > 0)
 
    r = requests.post(f"{BASE_URL}/copilot/query", json={"question": "What equipment is mentioned?"})
    answer_data = r.json()
    check("Copilot returns an answer", r.status_code == 200 and bool(answer_data.get("answer")))
    check("Copilot returns a trace", len(answer_data.get("trace", [])) > 0)
 
    r = requests.post(f"{BASE_URL}/copilot/query", json={"question": "What is the capital of France?"})
    guardrail_data = r.json()
    check(
        "Hallucination guardrail triggers on off-topic question",
        "don't have enough information" in guardrail_data.get("answer", "").lower(),
    )
 
    # --- Day 9-13 features ---
    if document_id:
        r = requests.post(f"{BASE_URL}/compliance/check/{document_id}")
        compliance_data = r.json()
        check("Compliance check returns summary", r.status_code == 200 and "summary" in compliance_data)
 
    r = requests.get(f"{BASE_URL}/rca/{equipment_tag}")
    rca_data = r.json()
    check(
        f"RCA returns hypotheses for {equipment_tag}",
        r.status_code == 200 and len(rca_data.get("hypotheses", [])) > 0,
    )
 
    r = requests.get(f"{BASE_URL}/alerts")
    check("Alerts endpoint responds", r.status_code == 200 and isinstance(r.json(), list))
 
    r = requests.get(f"{BASE_URL}/analytics/summary")
    analytics_data = r.json()
    check("Analytics summary has real data", analytics_data.get("total_documents", 0) > 0)
 
    r = requests.get(f"{BASE_URL}/audit-log")
    check("Audit log returns entries", r.status_code == 200 and len(r.json()) > 0)
 
    r = requests.get(f"{BASE_URL}/analytics/roi")
    roi_data = r.json()
    check("ROI endpoint returns hours_saved", "hours_saved" in roi_data)
 
    r = requests.post(f"{BASE_URL}/graph/detect-contradictions")
    check("Contradiction detector responds", r.status_code == 200 and isinstance(r.json(), list))
 
    print("\n" + ("=" * 40))
    passed = sum(results)
    print(f"{passed}/{len(results)} checks passed")
    if passed < len(results):
        sys.exit(1)
 
 
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python tests/smoke_test.py /path/to/test_document.pdf [EQUIPMENT_TAG]")
        sys.exit(1)
    tag = sys.argv[2] if len(sys.argv) > 2 else "P-204"
    run_smoke_test(sys.argv[1], tag)
