# 📄 **Part B — Sentiment Prompts & Results**

## **🔹 Prompt V1**

```text
You are a sentiment analysis assistant.

Return ONLY this JSON format:

{
  "sentiment": "positive" | "negative" | "neutral",
  "confidence": 0-100,
  "reasoning": "short explanation"
}

Rules:
- negative: complaints, frustration, delays, errors
- neutral: requests, questions, feature suggestions
- positive: appreciation or praise
- Output ONLY valid JSON.

Email:
""" {email} """
```

---

# ## **🔹 Prompt V1 — Results (12 Emails)**

### **Email 1**

```json
{
  "sentiment": "negative",
  "confidence": 90,
  "reasoning": "User cannot access a shared mailbox and sees permission errors."
}
```

### **Email 2**

```json
{
  "sentiment": "negative",
  "confidence": 90,
  "reasoning": "Workflow rules not working indicate a malfunction."
}
```

### **Email 3**

```json
{
  "sentiment": "negative",
  "confidence": 85,
  "reasoning": "Email stuck in pending suggests unresolved issues causing frustration."
}
```

### **Email 4**

```json
{
  "sentiment": "negative",
  "confidence": 95,
  "reasoning": "Automation creating duplicate tasks shows system malfunction."
}
```

### **Email 5**

```json
{
  "sentiment": "negative",
  "confidence": 95,
  "reasoning": "Missing tags indicates a broken feature."
}
```

### **Email 6**

```json
{
  "sentiment": "neutral",
  "confidence": 80,
  "reasoning": "Billing query without emotional language is neutral."
}
```

### **Email 7**

```json
{
  "sentiment": "negative",
  "confidence": 85,
  "reasoning": "CSAT scores disappearing indicates a possible outage."
}
```

### **Email 8**

```json
{
  "sentiment": "negative",
  "confidence": 90,
  "reasoning": "Email loading delays affect productivity and indicate a complaint."
}
```

### **Email 9**

```json
{
  "sentiment": "neutral",
  "confidence": 95,
  "reasoning": "Asking for help configuring SLAs is a neutral feature request."
}
```

### **Email 10**

```json
{
  "sentiment": "negative",
  "confidence": 90,
  "reasoning": "Mail merge failing prevents workflow, showing frustration."
}
```

### **Email 11**

```json
{
  "sentiment": "negative",
  "confidence": 90,
  "reasoning": "Authorization errors block adding users and indicate dissatisfaction."
}
```

### **Email 12**

```json
{
  "sentiment": "neutral",
  "confidence": 95,
  "reasoning": "Feature request for dark mode is neutral without negative sentiment."
}
```

---

#  **🔹 Improved Prompt V2**

```text
You are an expert sentiment-analysis system used in a customer support platform.

Classify sentiment STRICTLY using these definitions:

Sentiment Rules:
- negative → errors, outages, delays, complaints, billing problems, anything blocking work
- neutral → setup help, feature requests, configuration questions, information-only messages
- positive → appreciation, praise, strong satisfaction

Confidence scoring:
- 90–100 → clear emotional signal
- 70–89 → moderate clarity
- 50–69 → weak/uncertain

Output STRICT JSON ONLY:

{
  "sentiment": "positive" | "negative" | "neutral",
  "confidence": <number>,
  "reasoning": "internal explanation (not shown to the user)"
}

Rules:
- If neutral + negative signals appear, choose negative.
- If unsure between neutral and negative, choose negative.
- Only use emotional tone, not technical complexity.
- Do NOT output anything outside the JSON block.

Email:
""" {email} """
```