# 📊 GenAI-Dashboard-Generator

**GenAI-Dashboard-Generator** is an end-to-end Generative AI–powered analytics tool that allows users to interact with databases using natural language.  
It converts user questions into optimized SQL queries and automatically generates interactive dashboards — no SQL or BI tool expertise required.

---

## 🚀 Features

- 🔤 **Natural Language to SQL** using Generative AI
- 🧠 **LLM-powered query generation** (LLaMA 3 via Groq API)
- 📊 **Automatic dashboard creation** (bar, line, scatter charts)
- 🗄️ **SQLite database integration**
- ⚡ **Interactive Streamlit web app**
- 🔐 **Secure API key handling via `.env` or UI input**

---

## 🛠️ Tech Stack

- **Frontend & App Framework:** Streamlit  
- **LLM:** LLaMA 3.3 (70B) via Groq  
- **AI Orchestration:** LangChain  
- **Database:** SQLite  
- **Visualization:** Plotly  
- **Language:** Python  

---

## 📂 Project Structure
```
GenAI-Dashboard-Generator/
│
├── venv/ # Virtual environment
├── .env # Environment variables (Groq API Key)
├── app.py # Main Streamlit application
├── requirements.txt # Python dependencies
├── sales_data.db # SQLite database (auto-generated)
└── README.md # Project documentation
```
## 📦 Installation & Running Locally

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/GenAI-Dashboard-Generator.git
cd GenAI-Dashboard-Generator
### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Run the Streamlit App

```bash
streamlit run app.py
```

The app will open automatically in your browser.

---
🔗 **Streamlit App:**  
https://genai-dashboard-generator-shrytqdsgm5xhwxmgelkca.streamlit.app/

## ⭐ Acknowledgements

* UCI Machine Learning Repository
* Streamlit Community
* Scikit-learn Documentation

---

If you like this project, don’t forget to ⭐ the repository!

