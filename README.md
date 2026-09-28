# 🧠 Insight AI | Autonomous EDA Engine

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://eda-insightai.streamlit.app/)

**Insight AI** is an autonomous multi-agent data analysis and code execution engine. It allows you to ingest any CSV dataset and perform complex Exploratory Data Analysis (EDA), data cleaning, feature engineering, and visualization using plain English.

---

## 🚀 Live Demo

Try the live application here: **[https://eda-insightai.streamlit.app/](https://eda-insightai.streamlit.app/)**

You can upload your own dataset, or click "Load Sample Data" in the sidebar to try it out instantly with the Titanic dataset!

## ✨ Features

- **Multi-Agent Architecture:** Powered by Microsoft AutoGen, the system orchestrates a **Data Analyst Agent** (for reasoning and planning) and a **Code Executor Agent** (for writing and running code).
- **Secure Code Execution:** All generated Python code is securely executed in an ephemeral, sandboxed cloud environment provided by **E2B**. Your data and code are strictly isolated and purged after the session.
- **Natural Language EDA:** Ask complex questions like *"Impute missing values using the median and plot a correlation heatmap"* and watch the AI do the work.
- **Dynamic Visualizations:** Generates and displays both static plots and interactive HTML charts directly in the chat interface.
- **API Key Rotation:** Built-in resilient model client that automatically rotates Gemini/LLM API keys if rate limits or quotas are hit, ensuring uninterrupted analysis.

## 🛠️ Tech Stack

- **Frontend:** [Streamlit](https://streamlit.io/)
- **Agent Orchestration:** [AutoGen](https://microsoft.github.io/autogen/)
- **Secure Sandbox:** [E2B Cloud Code Interpreter](https://e2b.dev/)
- **LLM Integration:** Gemini via OpenAI-compatible SDK endpoints

## 💻 Local Setup & Installation

If you want to run Insight AI on your local machine:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/AnalyserGPT.git
   cd AnalyserGPT
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv eda_venv
   # Windows:
   .\eda_venv\Scripts\activate
   # Mac/Linux:
   source eda_venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   Create a `.env` file in the root directory and add your API keys:
   ```env
   E2B_API_KEY="your_e2b_api_key_here"
   GEMINI_API_KEY="your_primary_gemini_api_key_here"
   
   # Optional: Add fallback keys for automatic rotation if quotas are hit
   GEMINI_API_KEY_1="your_secondary_gemini_api_key_here"
   GEMINI_API_KEY_2="your_tertiary_gemini_api_key_here"
   ```

5. **Run the application:**
   ```bash
   streamlit run app.py
   ```

## 🛡️ Privacy & Security
Insight AI utilizes E2B's secure cloud sandboxes. When you upload a dataset, it is securely transferred to an isolated Docker container for the duration of your session. Once the analysis is complete or the session is closed, the sandbox and all associated data are permanently destroyed.

## 👨‍💻 Developers
Built with ❤️ by Kartik & Harshil.
