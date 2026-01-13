from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
from config import settings 

client = OpenAI(api_key=settings.openai_api_key)

app = FastAPI()

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
def chat(req: ChatRequest):
    response = client.chat.completions.create(
        model = "gpt-4o-mini",
        messages = [
            {"role": "user", "content": req.message}
        ]
    )

    return {
        "reply": response.choices[0].message.content
    }