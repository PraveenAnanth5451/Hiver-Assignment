# **Hiver AI Intern Assignment – Complete Submission**

This repository contains my full solution to the **Hiver AI Intern Evaluation Assignment**, covering all three required components:

* **Part A – Email Tagging Mini-System**
* **Part B – Sentiment Analysis Prompt Evaluation**
* **Part C – Retrieval-Augmented Generation (RAG) System**

Each part includes code, documentation, results, and improvement ideas as requested.

---

# **📁 Repository Structure**

```
HIVER/
│
├── PART_A/
│   ├── part1.py
│   ├── partA_readme.md
│   └── partA.docx (optional)
│
├── PART_B/
│   ├── partB_readme.md
│   └── partB.docx (optional)
│
├── PART_C/
│   ├── part3_gemini_rag.py
│   ├── partC_readme.md
│   ├── kb_articles/
│   │     ├── automation_setup.txt
│   │     └── csat_troubleshooting.txt
│   └── part3_results.json (optional)
│
├── emails.csv
├── large_emails.csv
├── predictions.csv
└── requirements.txt
```

---

# **Part A – Email Tagging Mini-System**

**Goal:**
Build a simple baseline classifier for tagging support emails while ensuring **customer isolation** (tags from one customer should not leak into another customer’s predictions).

### ✔ Key Features

* TF–IDF + Linear SVM model trained **per customer**
* Rule-based **pattern matcher** before ML fallback
* Optional LLM fallback (OpenAI/Gemini)
* Customer-isolated training and prediction
* Error analysis & improvement ideas included

### ✔ Files

* `PART_A/part1.py`
* `PART_A/partA_readme.md`

### ✔ How to run

```
python PART_A/part1.py
```

---

#  **Part B – Sentiment Analysis Prompt Evaluation**

**Goal:**
Design and test sentiment prompts for LLMs to evaluate consistency, accuracy, and explainability.

### ✔ Includes

* Prompt V1
* Results for 12 emails
* Improved Prompt V2
* Results for 12 emails
* 1-page report:

  * What failed
  * What improved
  * How to systematically evaluate prompts

### ✔ Files

* `PART_B/partB_readme.md`

---

# **Part C – RAG System (Knowledge Retrieval)**

**Goal:**
Build a simple retrieval pipeline using embeddings and generate answers grounded in KB articles.

### ✔ Steps Implemented

* Load KB articles from folder
* Generate Gemini embeddings
* Compute cosine similarity
* Retrieve most relevant documents
* Generate grounded answer with confidence score
* Provide improvement ideas and a failure-case debugging walkthrough

### ✔ Files

* `PART_C/part3_gemini_rag.py`
* `PART_C/partC_readme.md`
* `PART_C/kb_articles/*.txt`

### ✔ How to run

```
python PART_C/part3_gemini_rag.py
```

---

#  **🔧 Requirements**

Install dependencies:

```
pip install -r requirements.txt
```

Set your Gemini key:

```
setx GEMINI_API_KEY "your_key_here"   # Windows
export GEMINI_API_KEY="your_key_here" # Mac/Linux
```

---

# **🧠 Summary**

This assignment includes:

* 📌 A customer-isolated tagging model (Part A)
* 📌 Improved LLM sentiment prompting (Part B)
* 📌 A working retrieval and answer-generation pipeline (Part C)
* 📌 Clean documentation, reproducible code, and grounded analysis

I thoroughly enjoyed working on this challenge especially the mix of ML, LLM prompting, embeddings, and RAG design.

