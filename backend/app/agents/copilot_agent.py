"""
Expert Copilot Agent
----------------------
Inputs:   User natural-language query
Outputs:  Cited, confidence-scored answer
Memory:   Reads Vector DB (ChromaDB) for retrieval
Talks to: Orchestrator, Knowledge Graph Agent (later phases)
"""
import json

from groq import Groq

from app.core.config import settings
from app.db.vector_store import query_chunks

client = Groq(api_key=settings.llm_api_key)

ANSWER_PROMPT = """You are OpsBrain's Expert Copilot, an industrial operations assistant.
Answer the question using ONLY the context chunks below. Each chunk is labeled with
its source document.

If the context does not contain enough information to answer confidently, respond
exactly with: "I don't have enough information in the ingested documents to answer that."
Do not guess or use outside knowledge.

Return ONLY a JSON object, no markdown fences, with these exact keys:
- "answer": your answer as a string
- "confidence": a number from 0.0 to 1.0 reflecting how well the context supports the answer
- "citations": an array of objects, each with "document" (filename) and "snippet"
  (the exact short phrase from the context that supports the answer, under 20 words)

Context chunks:
{context}

Question: {question}
"""


class CopilotAgent:
    def answer(self, question: str, k: int = 5) -> dict:
        results = query_chunks(question, top_k=k)

        if not results["documents"][0]:
            return {
                "answer": "I don't have enough information in the ingested documents to answer that.",
                "confidence": 0.0,
                "citations": [],
            }

        context_blocks = []
        for doc_text, meta in zip(results["documents"][0], results["metadatas"][0]):
            context_blocks.append(f"[Source: {meta['filename']}]\n{doc_text}")
        context = "\n---\n".join(context_blocks)

        prompt = ANSWER_PROMPT.format(context=context, question=question)
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}],
        )

        raw = response.choices[0].message.content.strip()
        raw = raw.removeprefix("```json").removeprefix("```").removesuffix("```").strip()

        try:
            parsed = json.loads(raw)
        except json.JSONDecodeError:
            parsed = {
                "answer": "I encountered an error parsing the response. Please try rephrasing your question.",
                "confidence": 0.0,
                "citations": [],
            }

        return parsed