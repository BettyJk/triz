# ⚙️ TRIZ Engineering Problem Solver

> Smart solutions for real-world engineering contradictions — powered by Groq's LLaMA3 and TRIZ methodology.

This app uses the **TRIZ 40 Principles** and the **contradiction matrix** to help engineers and innovators find **creative, real-life solutions** to problems involving tradeoffs or conflicting requirements. It combines classical TRIZ logic with state-of-the-art **LLM analysis** to suggest practical strategies based on your input.

![Streamlit Screenshot](https://placehold.co/600x300?text=App+Screenshot) <!-- Replace this with your actual screenshot -->

---

## 🚀 Features

- 🔍 **AI-Powered Parameter Detection**  
  Uses LLaMA3 to identify key engineering parameters from your problem statement.

- 🧠 **Contradiction Matrix Matching**  
  Automatically identifies contradictions and fetches relevant TRIZ principles.

- 💡 **Real-World Examples from AI**  
  Generates specific, realistic engineering strategies tailored to the problem and industry (e.g., automotive, aerospace).

- 📊 **Optimal Recommendation**  
  Recommends the most effective TRIZ principle for your case with explanation.

---

## 📦 Tech Stack

- [Streamlit](https://streamlit.io/) — UI for fast, interactive prototyping  
- [Groq API](https://console.groq.com/) — LLM backend using LLaMA3  
- Python 🐍  
- JSON-based TRIZ data structure  
- `difflib` for fuzzy matching fallback when AI isn't confident  

---

## 🔧 Setup Instructions

> First, clone the repo and make sure your Python environment is active.

```bash
git clone https://github.com/BettyJk/triz.git
cd triz
pip install -r requirements.txt
