"""
Knowledge Graph Agent (v2 — Day 5, Day 13 — Contradiction Detector)
--------------------------------------------------------------------
Inputs:   Document metadata + extracted entities
Outputs:  Updated graph nodes/edges, plus CONFLICTS_WITH edges when the
          same entity value is seen under two different entity_types,
          and CONFLICTS_WITH edges between Documents when an LLM
          confirms they genuinely contradict each other about shared equipment
Memory:   Persistent (Neo4j = long-term memory)
Talks to: Expert Copilot Agent, RCA Agent, Compliance Agent, Groq LLM

New in v2:
- reference_count on each Entity node (how many documents mention it)
- CONFLICTS_WITH relationship when a value is tagged inconsistently
  across documents

New in Day 13:
- Cross-document contradiction detection using Groq, writes
  CONFLICTS_WITH edges between Document nodes when real conflicts are found
"""
import json
import re

from groq import Groq

from app.core.config import settings
from app.db.neo4j_client import neo4j_client
from app.db.vector_store import _collection as collection

client = Groq(api_key=settings.llm_api_key)


CONTRADICTION_PROMPT = """Two document excerpts both mention equipment {tag}.
Do they contradict each other (e.g. conflicting specs, conflicting maintenance
status, conflicting instructions)?

Excerpt A: {text_a}
Excerpt B: {text_b}

Return ONLY a JSON object, no markdown fences, no preamble:
{{"contradicts": true or false, "reason": "short explanation"}}
"""


class KnowledgeGraphAgent:
    def merge(self, document_id: str, filename: str, entities: list[dict]) -> dict:
        neo4j_client.run_query(
            "MERGE (d:Document {id: $document_id}) SET d.filename = $filename",
            {"document_id": document_id, "filename": filename},
        )

        conflicts = []

        for entity in entities:
            value = entity.get("value")
            entity_type = entity.get("entity_type")
            confidence = entity.get("confidence", 0.0)

            existing = neo4j_client.run_query(
                "MATCH (e:Entity {value: $value}) WHERE e.entity_type <> $entity_type "
                "RETURN e.entity_type AS existing_type LIMIT 1",
                {"value": value, "entity_type": entity_type},
            )
            if existing:
                conflicts.append(
                    {
                        "value": value,
                        "new_type": entity_type,
                        "existing_type": existing[0]["existing_type"],
                    }
                )

            neo4j_client.run_query(
                """
                MERGE (e:Entity {value: $value, entity_type: $entity_type})
                ON CREATE SET e.confidence = $confidence, e.reference_count = 1
                ON MATCH SET e.reference_count = coalesce(e.reference_count, 1) + 1
                WITH e
                MATCH (d:Document {id: $document_id})
                MERGE (d)-[:CONTAINS]->(e)
                """,
                {
                    "value": value,
                    "entity_type": entity_type,
                    "confidence": confidence,
                    "document_id": document_id,
                },
            )

        for c in conflicts:
            neo4j_client.run_query(
                """
                MATCH (a:Entity {value: $value, entity_type: $new_type})
                MATCH (b:Entity {value: $value, entity_type: $existing_type})
                MERGE (a)-[:CONFLICTS_WITH]->(b)
                """,
                c,
            )

        return {"status": "merged", "entity_count": len(entities), "conflicts_found": len(conflicts)}

    def get_cross_referenced_entities(self, min_references: int = 2) -> list[dict]:
        results = neo4j_client.run_query(
            """
            MATCH (e:Entity)
            WHERE e.reference_count >= $min_references
            RETURN e.value AS value, e.entity_type AS entity_type, e.reference_count AS reference_count
            """,
            {"min_references": min_references},
        )
        return [
            {
                "value": r["value"],
                "entity_type": r["entity_type"],
                "reference_count": r["reference_count"],
            }
            for r in results
        ]

    def _ask_llm_for_contradiction(self, equipment_tag: str, text_a: str, text_b: str) -> dict:
        prompt = CONTRADICTION_PROMPT.format(tag=equipment_tag, text_a=text_a[:400], text_b=text_b[:400])
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            max_tokens=256,
            messages=[{"role": "user", "content": prompt}],
        )
        raw = response.choices[0].message.content.strip()
        raw = raw.removeprefix("```json").removeprefix("```").removesuffix("```").strip()
        match = re.search(r"\{.*\}", raw, re.DOTALL)
        if not match:
            return {"contradicts": False, "reason": ""}
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            try:
                return json.loads(match.group(0).strip())
            except json.JSONDecodeError:
                print("RAW GROQ RESPONSE (unparseable):", repr(raw))
                return {"contradicts": False, "reason": ""}

    def detect_contradictions(self) -> list[dict]:
        cross_referenced = self.get_cross_referenced_entities()
        equipment_entities = [e for e in cross_referenced if e["entity_type"] == "equipment_tag"]
        findings = []

        for entity in equipment_entities:
            docs = neo4j_client.run_query(
                """
                MATCH (d:Document)-[:CONTAINS]->(e:Entity {value: $val, entity_type: 'equipment_tag'})
                RETURN d.id AS doc_id, d.filename AS filename
                """,
                {"val": entity["value"]},
            )
            if len(docs) < 2:
                continue

            doc_a, doc_b = docs[0], docs[1]

            chunk_a = collection.query(
                query_texts=[entity["value"]], n_results=1, where={"document_id": doc_a["doc_id"]}
            )
            chunk_b = collection.query(
                query_texts=[entity["value"]], n_results=1, where={"document_id": doc_b["doc_id"]}
            )

            if not chunk_a["documents"][0] or not chunk_b["documents"][0]:
                continue

            result = self._ask_llm_for_contradiction(
                entity["value"], chunk_a["documents"][0][0], chunk_b["documents"][0][0]
            )

            if result.get("contradicts"):
                neo4j_client.run_query(
                    """
                    MATCH (a:Document {id: $doc_a}), (b:Document {id: $doc_b})
                    MERGE (a)-[r:CONFLICTS_WITH]->(b)
                    SET r.kind = 'conflict', r.reason = $reason, r.equipment_tag = $tag
                    """,
                    {
                        "doc_a": doc_a["doc_id"],
                        "doc_b": doc_b["doc_id"],
                        "reason": result.get("reason", ""),
                        "tag": entity["value"],
                    },
                )
                findings.append(
                    {
                        "equipment_tag": entity["value"],
                        "document_a": doc_a["filename"],
                        "document_b": doc_b["filename"],
                        "reason": result.get("reason", ""),
                    }
                )

        return findings