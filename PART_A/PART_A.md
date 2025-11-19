# 📄 **README — Part A: Email Tagging Mini-System**

## **1. Approach**

The goal was to build a simple but reliable email-tagging system while ensuring strict **customer isolation**.
The final design uses a **hybrid pipeline** combining:

1. **Pattern-based rules** → fast, keyword-driven tagging for obvious cases (e.g., “permission denied → access_issue”).
2. **Per-customer ML classifier** → a TF-IDF + Linear SVM model trained **separately for each customer_id**, preventing tag leakage across customers.
3. **Optional LLM fallback** → if both pattern and ML are uncertain, an LLM is prompted with **only the allowed tags for that customer**.

This hybrid design gives strong accuracy even with small datasets.

---

## **2. Model / Prompt**

### **ML Model**

* **TF-IDF Vectorizer** for text features
* **Linear SVM** for classification
* One model **per customer** instead of one global model

This creates multiple small customer-specific classifiers.

### **LLM Prompt (for fallback classification)**

```
You are an email tagging assistant for customer <customer_id>.
Allowed tags: <list_of_customer_specific_tags>.

Read the email and select exactly ONE tag from the allowed list.

Email:
<subject + body>
```

This constraint ensures the LLM cannot output irrelevant tags.

---

## **3. Ensuring Customer Isolation**

Customer isolation is enforced in three layers:

1. **Separate Models per Customer**
   Each customer’s data is used to train its own model.
   No cross-customer learning or tag contamination.

2. **Customer-Specific Allowed Tags**
   During prediction, the model (patterns, ML, LLM) can ONLY pick from tags belonging to that customer.

3. **Independent Vectorizers**
   TF-IDF vocabulary is generated separately per customer, preventing text leakage.

This guarantees isolation at data, model, and inference levels.

---

## **4. Error Analysis**

### **Observed Issues**

* Similar vocabulary across tags (e.g., “pending”, “workflow”, “status”) occasionally confuses the model.
* Very short emails sometimes lack enough signal → fallback needed.
* Some tags rely heavily on specific keywords, making patterns important.

### **Common Failure Patterns**

* Mixed-intent emails (“billing + workflow issue”) → ambiguous classification
* Emails with general wording (“something is wrong”) → ML struggles without context

### **Fixes Implemented**

* Added keyword-based patterns for strong signals
* Added anti-patterns to prevent misleading words
* Introduced LLM fallback with restricted tags
* Provided customer-specific tag lists to reduce confusion

This significantly stabilized predictions across small samples.

