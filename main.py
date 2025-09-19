import os
import re
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
from langchain.prompts import FewShotPromptTemplate, PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

# Load environment variables
load_dotenv()
gemini_api_key = os.getenv("GOOGLE_API_KEY")
if not gemini_api_key:
    raise ValueError("❌ No GOOGLE_API_KEY found. Please set it in your .env file")

# Initialize Gemini model
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key=gemini_api_key,
    temperature=0.2
)

# Categories
CATEGORIES = ["password_reset", "login_problem", "hr_query"]

# Few-shot examples
examples = [
    {"input": "I forgot my password and need to reset it.", "output": "password_reset"},
    {"input": "My login isn't working because of a wrong password.", "output": "login_problem"},
    {"input": "How do I check my remaining leave days?", "output": "hr_query"},
    {"input": "The printer is not working", "output": "unknown"},
]

# Prompt templates
example_template = PromptTemplate(
    input_variables=["input", "output"],
    template="Ticket: {input}\nCategory: {output}\n"
)

classify_prompt = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_template,
    prefix="Classify the support ticket into one of: password_reset, login_problem, hr_query, unknown.\n",
    suffix="Ticket: {user_input}\nCategory:",
    input_variables=["user_input"]
)

response_prompt = PromptTemplate(
    input_variables=["ticket_text", "category"],
    template=(
        "Based on category '{category}', provide a 3-step response for: {ticket_text}\n\n"
        "- password_reset: login page → 'Forgot Password' → follow instructions\n"
        "- login_problem: check password → suggest resetting → contact support\n"
        "- hr_query: hr.mycompany.com → login → navigate\n"
        "- unknown: explain it’s outside scope and suggest proper support\n"
        "Use numbered steps."
    )
)

def normalize_category(category_text: str) -> str:
    """Clean and match category"""
    if not category_text:
        return "unknown"
    category_text = category_text.strip().lower()
    category_text = re.sub(r'[^a-zA-Z_]', '', category_text)
    return category_text if category_text in CATEGORIES else "unknown"

def process_ticket(ticket_text: str) -> tuple[str, str]:
    """Classify ticket and generate response"""
    try:
        # Classify
        raw_category = llm.invoke(classify_prompt.format(user_input=ticket_text)).content.strip()
        category = normalize_category(raw_category)

        # Generate response
        response = llm.invoke(response_prompt.format(ticket_text=ticket_text, category=category)).content.strip()
        return category, response
    except Exception as e:
        return "unknown", f"⚠️ Error: {str(e)}"

# ---------------- FASTAPI ----------------
app = FastAPI(title="Smart Ticket Classifier")

class TicketRequest(BaseModel):
    text: str

class TicketResponse(BaseModel):
    category: str
    response: str

@app.post("/classify", response_model=TicketResponse)
async def classify_ticket(req: TicketRequest):
    category, response = process_ticket(req.text)
    return {"category": category, "response": response}

@app.get("/")
async def root():
    return {"message": "Smart Ticket Classifier API is running 🚀"}
