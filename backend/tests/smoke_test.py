"""
Full Pipeline Smoke Test
--------------------------
Run this against a running local backend (uvicorn on port 8000) to verify
the entire pipeline works end-to-end: health checks, upload, entity
extraction, graph writes, embeddings, and Copilot Q&A — including the
hallucination guardrail.
 
Usage:
    python tests/smoke_test.py /path/to/a/test_document.pdf
 
Rerun this unchanged on Day 14 and Day 18 to catch regressions.
"""
import sys
import requests
 
BASE_URL = "http://localhost:8000/api"
 
 
def check(label: str, condition: bool, extra: str = "") -> bool:
    status = "PASS" if condition else "FAIL"
    print(f"[{status}] {label} {extra}")
    return condition
 
 
def run_smoke_test(test_file_path: str):
    results = []
 
    r = requests.get(f"{BASE_URL}/health")
    results.append(check("GET /health", r.status_code == 200 and r.json().get("status") == "ok"))
 
    r = requests.get(f"{BASE_URL}/db-health")
    data = r.json()
    results.append(check("Postgres connected", data.get("postgres") == "connected"))
    results.append(check("Neo4j connected", data.get("neo4j") == "connected"))
 
    with open(test_file_path, "rb") as f:
        r = requests.post(f"{BASE_URL}/documents/upload", files={"file": f})
    upload_data = r.json()
    results.append(check("Document upload", r.status_code == 200 and upload_data.get("status") == "processed"))
    results.append(
        check(
            "Entities extracted",
            upload_data.get("entity_count", 0) > 0,
            f"(entity_count={upload_data.get('entity_count')})",
        )
    )
 
    r = requests.get(f"{BASE_URL}/documents")
    results.append(check("GET /documents returns list", r.status_code == 200 and len(r.json()) > 0))
 
    r = requests.get(f"{BASE_URL}/graph")
    graph_data = r.json()
    results.append(check("Graph has nodes", len(graph_data.get("nodes", [])) > 0))
 
    r = requests.post(f"{BASE_URL}/copilot/query", json={"question": "What equipment is mentioned?"})
    answer_data = r.json()
    results.append(check("Copilot returns an answer", r.status_code == 200 and bool(answer_data.get("answer"))))
    results.append(check("Copilot returns a trace", len(answer_data.get("trace", [])) > 0))
 
    r = requests.post(f"{BASE_URL}/copilot/query", json={"question": "What is the capital of France?"})
    guardrail_data = r.json()
    results.append(
        check(
            "Hallucination guardrail triggers on off-topic question",
            "don't have enough information" in guardrail_data.get("answer", "").lower(),
        )
    )
 
    print("\n" + ("=" * 40))
    passed = sum(results)
    print(f"{passed}/{len(results)} checks passed")
    if passed < len(results):
        sys.exit(1)
 
 
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python tests/smoke_test.py /path/to/test_document.pdf")
        sys.exit(1)
    run_smoke_test(sys.argv[1])
