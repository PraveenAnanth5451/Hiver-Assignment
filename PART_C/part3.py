import os
import glob
import json
import numpy as np
import google.generativeai as genai


API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise Exception("GEMINI_API_KEY not set.")

genai.configure(api_key=API_KEY)

EMBED_MODEL = "models/text-embedding-004"
GEN_MODEL   = "models/gemini-2.5-flash"
TOP_K = 3

# Utility

def load_kb(folder="PART_C\kb_articles"):
    files = glob.glob(f"{folder}/*.*")
    docs = []
    for f in files:
        with open(f, "r", encoding="utf-8") as fp:
            text = fp.read().strip()
        docs.append({"id": os.path.basename(f), "text": text})
    return docs


def embed(text):
    """Generate Gemini embedding for a single text."""
    res = genai.embed_content(
        model=EMBED_MODEL,
        content=text,
        task_type="retrieval_document"
    )
    return np.array(res["embedding"], dtype=float)


def cosine(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-8)

# Build embedding index

def build_index(docs):
    print("Building embeddings for KB articles...")
    for d in docs:
        d["embedding"] = embed(d["text"])
    return docs

# Retrieve
def retrieve(query, docs, top_k=TOP_K):
    q_emb = embed(query)
    scored = []
    for d in docs:
        score = float(cosine(q_emb, d["embedding"]))
        scored.append({"id": d["id"], "text": d["text"], "score": score})

    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[:top_k]

def generate_answer(query, retrieved_docs):
    context = "\n\n".join(
        [f"### {d['id']}\n{d['text']}" for d in retrieved_docs]
    )

    prompt = f"""
You are a helpful assistant. Answer the user's question using ONLY the KB context provided.

KB CONTEXT:
{context}

Question: {query}

Provide a short factual answer (3–6 sentences).
Do NOT hallucinate. If answer is not in context, say: "Information not found in KB."

Also list which article IDs were used.

Return JSON only:
{{
  "answer": "...",
  "sources": ["id1","id2"],
  "confidence": 0-100
}}
"""

    response = genai.GenerativeModel(GEN_MODEL).generate_content(prompt)
    return response.text.strip()

# Confidence score = top similarity × 100
def compute_confidence(retrieved):
    if not retrieved:
        return 0
    return round(max(d["score"] for d in retrieved) * 100, 2)

def main():
    docs = load_kb()
    if not docs:
        print("No KB documents found in 'kb_articles/' folder.")
        return

    docs = build_index(docs)

    queries = [
        "How do I configure automations in Hiver?",
        "Why is CSAT not appearing?"
    ]

    results = []

    for q in queries:
        print("\n" + "="*60)
        print("QUERY:", q)

        retrieved = retrieve(q, docs)
        print("\nTop Retrieved Articles:")
        for r in retrieved:
            print(f"- {r['id']} (score={r['score']:.4f})")

        confidence = compute_confidence(retrieved)
        print(f"\nRetrieval Confidence: {confidence}/100")

        answer = generate_answer(q, retrieved)
        print("\nGenerated Answer:")
        print(answer)

        results.append({
            "query": q,
            "retrieved": retrieved,
            "confidence": confidence,
            "answer": answer
        })

    # Save output
    with open("part3_gemini_rag_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print("\nSaved → part3_gemini_rag_results.json")


if __name__ == "__main__":
    main()
