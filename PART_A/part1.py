import os
import re
import pandas as pd
from collections import defaultdict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score
from sklearn.pipeline import Pipeline

# Optional LLM
try:
    import openai
    USE_OPENAI = True
    openai.api_key = os.getenv("OPENAI_API_KEY")
except Exception:
    USE_OPENAI = False


# CLEAN + LOAD
def load_data(csv_path="large_emails.csv"):
    df = pd.read_csv(csv_path)

    # Strip hidden column spaces
    df.columns = df.columns.str.strip()

    # Validate required columns
    required_cols = {"email_id", "customer_id", "subject", "body", "tag"}
    if not required_cols.issubset(set(df.columns)):
        print("\n❌ ERROR: CSV columns incorrect.")
        print("Found columns:", df.columns.tolist())
        raise SystemExit

    df["text"] = (df["subject"].fillna("") + " " +
                df["body"].fillna("")).apply(clean_text)

    return df


def clean_text(s):
    if not isinstance(s, str):
        return ""
    s = s.lower()
    s = re.sub(r"\s+", " ", s)
    return s.strip()
PATTERNS = {
    "access_issue": ["access", "permission", "login"],
    "workflow_issue": ["workflow", "rule"],
    "status_bug": ["pending", "stuck"],
    "automation_bug": ["automation", "duplicate"],
    "billing": ["billing", "invoice", "charged"],
    "billing_error": ["mismatch", "invoice"],
    "analytics_issue": ["analytics", "csat", "report"],
    "performance": ["slow", "delay", "lag"],
    "ui_bug": ["ui", "freeze", "glitch"],
    "tagging_issue": ["tag"],
    "mail_merge_issue": ["mail merge"],
    "user_management": ["add user", "authorization"],
    "feature_request": ["feature request", "please consider"],
}

def pattern_match(text, allowed_tags):
    for tag in allowed_tags:
        if tag in PATTERNS:
            for kw in PATTERNS[tag]:
                if kw in text:
                    return tag
    return None

def llm_predict(text, allowed_tags):
    if not USE_OPENAI:
        return None  

    prompt = f"""
You are an email tagging assistant.

Allowed tags: {', '.join(allowed_tags)}

Email:
{text}

Return ONLY one tag exactly from the allowed tags.
"""

    try:
        res = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )
        tag = res.choices[0].message["content"].strip()
        return tag
    except Exception as e:
        print("LLM Error:", e)
        return None
# TRAIN ML MODEL PER CUSTOMER
def train_models(df):
    models = {}
    for cust, subdf in df.groupby("customer_id"):
        tfidf = TfidfVectorizer(stop_words="english")
        svm = LinearSVC()

        pipe = Pipeline([("tfidf", tfidf), ("svm", svm)])
        pipe.fit(subdf["text"], subdf["tag"])
        models[cust] = pipe

    return models
# FINAL PREDICTOR PIPELINE
def predict(df, models):
    preds = []
    for _, row in df.iterrows():
        text = row["text"]
        cust = row["customer_id"]
        allowed = list(df[df["customer_id"] == cust]["tag"].unique())

        pat = pattern_match(text, allowed)
        if pat:
            preds.append(pat)
            continue

        ml_pred = models[cust].predict([text])[0]
        preds.append(ml_pred)
        continue

    return preds


# MAIN
def main():
    print("Loading data...")
    df = load_data()

    print("Training customer-isolated models...")
    models = train_models(df)

    print("Predicting...")
    df["pred"] = predict(df, models)

    acc = accuracy_score(df["tag"], df["pred"])
    print("\nAccuracy:", acc)

    print("\nPredictions:")
    print(df[["email_id", "customer_id", "tag", "pred"]])

    df.to_csv("predictions.csv", index=False)
    print("\nSaved predictions.csv successfully.")


if __name__ == "__main__":
    main()
