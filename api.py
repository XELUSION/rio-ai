from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import Groq

app = FastAPI()
client = Groq(api_key="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")

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

class Message(BaseModel):
    message: str

conversation = [
    {"role": "system", "content": "Kamu asisten AI yang helpful."}
]

@app.get("/")
def root():
    return {"status": "Rio AI is running!"}

@app.post("/chat")
def chat(body: Message):
    conversation.append({"role": "user", "content": body.message})
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=conversation
    )
    reply = response.choices[0].message.content
    conversation.append({"role": "assistant", "content": reply})
    return {"reply": reply}