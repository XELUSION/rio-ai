from groq import Groq

client = Groq(api_key="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")

# Baca file sebagai "pengetahuan" AI
with open("data.txt", "r") as f:
    knowledge = f.read()

conversation = [
    {
        "role": "system",
        "content": f"Kamu adalah asisten AI. Gunakan informasi ini untuk menjawab pertanyaan:\n\n{knowledge}"
    }
]

print("AI siap! Ketik 'exit' untuk keluar.\n")

while True:
    user_input = input("Kamu: ")
    if user_input.lower() == "exit":
        break
    
    conversation.append({"role": "user", "content": user_input})
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=conversation
    )
    reply = response.choices[0].message.content
    conversation.append({"role": "assistant", "content": reply})
    print(f"AI: {reply}\n")