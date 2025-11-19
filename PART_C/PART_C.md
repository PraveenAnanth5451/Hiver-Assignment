# 📄 **Part C – Retrieval Improvements & Debugging Report**

## **1. Five Ways to Improve Retrieval Quality**

1. **Document Chunking for Finer Granularity**
   Split long KB articles into smaller chunks (200–300 tokens). This reduces noise and allows the retriever to focus on specific sections instead of entire documents, improving accuracy for specific queries.

2. **Hybrid Retrieval: BM25 + Embeddings + Reranking**
   Combine a lexical retriever (BM25) with semantic embeddings. Retrieve top documents from both methods and use a small LLM or cross-encoder to rerank them. This significantly boosts recall and reduces missed relevant articles.

3. **Query Expansion Using LLM Rewrites**
   Automatically generate synonyms, paraphrases, and expanded versions of the query. This helps match KB articles even when vocabulary differs (e.g., “CSAT not appearing” vs “missing survey responses”).

4. **Metadata Filtering & Categorization**
   Tag KB articles with metadata such as category (analytics, automation, workflow, billing). Filter retrieval by category before calculating similarity scores. This prevents unrelated documents from appearing in top results.

5. **Embedding Monitoring & Index Versioning**
   Regularly evaluate embedding quality and detect drift. Rebuild the embedding index when KB content changes or new articles are added. Version the index to ensure reproducibility and rollback safety.

---

## **2. Failure Case & Debugging Steps**

### **Failure Case: Incorrect Retrieval for CSAT Query**

**Query:**
“Why is CSAT not appearing?”

**Issue:**
The retrieval returned unrelated articles (e.g., automation setup) and the generated answer was not grounded in any CSAT-related content.
This led to an incorrect or hallucinated answer.

---

### **Debugging Steps**

1. **Check Retrieval Scores**
   Inspect similarity values. If the top score is below **0.25**, retrieval likely failed because embeddings didn’t match the query vocabulary.

2. **Verify Relevant KB Content Exists**
   Confirm that KB contains at least one CSAT-related article with words like “survey”, “customer satisfaction”, or “feedback”.

3. **Inspect Embedding Generation**
   Ensure the embedding model indexed all KB articles correctly and no file was skipped or truncated.

4. **Test Query Reformulation**
   Rephrase the query (“CSAT missing”, “survey not showing”, “feedback reports not appearing”) and see if retrieval improves.
   If results improve, add synonym mapping or query expansion.

5. **Add Domain-Specific Keywords / Boosting Rules**
   If CSAT-related keywords (“survey”, “rating”, “feedback”) are not weighted enough, add boosting rules to improve similarity scoring for these terms.

---
