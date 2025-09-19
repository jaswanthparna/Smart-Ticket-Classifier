🎫 Smart Ticket Classifier

An AI-powered support ticket classification system built with FastAPI, Streamlit, and Google Gemini AI.
This tool automatically categorizes support tickets (e.g., password issues, login problems, HR queries) and generates step-by-step responses.

🚀 Features

✅ Classifies tickets into:
🔐 Password Reset
🔑 Login Problems
👥 HR Queries
❓ Unknown

✅ Generates AI-based step-by-step responses

✅ REST API with FastAPI

✅ Web UI with Streamlit

✅ Environment variable management via .env

⚙️ Setup
1. Clone the repository
https://github.com/jaswanthparna/Smart-Ticket-Classifier.git
cd Smart-Ticket-Classifier

2. Create virtual environment
python -m venv venv
venv\Scripts\activate      # Windows

3. Install dependencies
pip install -r requirements.txt

4. Add your API key

Create a .env file in the project root:

GOOGLE_API_KEY=your_google_gemini_api_key_here

▶️ Running the App
Run Backend (FastAPI):
uvicorn main:app --reload


API available at: http://127.0.0.1:8000

Swagger docs: http://127.0.0.1:8000/docs

Run Frontend (Streamlit):
streamlit run frontend.py

Local URL: http://localhost:8501

output:

![alt text](<Screenshot 2025-09-19 175900.png>)