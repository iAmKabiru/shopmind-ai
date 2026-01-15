from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
from config import settings 

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


@app.post("/chat")
def chat(req: ChatRequest):
    response = client.chat.completions.create(
        model = openai_model,
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": req.message}
        ]
    )

    return {
        "reply": response.choices[0].message.content
    }