from fastapi import FastAPI
from pydantic import BaseModel  
from openai import OpenAI
from config import settings 
from data import PRODUCTS, REVIEWS

client = OpenAI(api_key=settings.openai_api_key)
openai_model = settings.openai_model

app = FastAPI()

class ChatRequest(BaseModel):
    message: str


SYSTEM_PROMPT = """
You are ShopMind, a senior ecommerce business analyst.

You help online stores:
- Increase sales
- Avoid stockouts
- Optimize pricing
- Understand customer behavior

Always respond in this format:

1. Insight
2. Risk
3. Recommendation

Use simple, clear business language.
"""

def retrieve_context(question: str):
    context = ""

    for p in PRODUCTS:
        context += f"Product: {p['name']}, stock: {p['stock']}, price: {p['price']}\n"

    for r in REVIEWS:
        context += f"Review: {r['text']}\n"

    return context

@app.post("/chat")
def chat(req: ChatRequest):
    context = retrieve_context(req.message)


    response = client.chat.completions.create(
        model = openai_model,
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "system", "content": f"Store Data:\n{context}"},
            {"role": "user", "content": req.message}
        ]
    )

    return {
        "reply": response.choices[0].message.content
    }