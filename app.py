from flask import Flask, request, jsonify, render_template_string
from groq import Groq

app = Flask(__name__)
client = Groq(api_key="GROQ_API_KEY")

conversation = [
    {"role": "system", "content": "Kamu adalah asisten AI yang ramah dan helpful. Jawab dalam bahasa Indonesia."}
]

HTML = """
<!DOCTYPE html>
<html>
<head><title>Rio AI</title></head>
<body style="font-family: Arial; max-width: 600px; margin: 50px auto;">
    <h2>💬 Rio AI Chatbot</h2>
    <div id="chat" style="border: 1px solid #ccc; height: 400px; overflow-y: scroll; padding: 10px; margin-bottom: 10px;"></div>
    <input id="msg" type="text" style="width: 80%;" placeholder="Ketik pesan...">
    <button onclick="send()">Kirim</button>
    <script>
        async function send() {
            const msg = document.getElementById('msg').value;
            document.getElementById('chat').innerHTML += `<p><b>Kamu:</b> ${msg}</p>`;
            document.getElementById('msg').value = '';
            const res = await fetch('/chat', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({message: msg})});
            const data = await res.json();
            document.getElementById('chat').innerHTML += `<p><b>AI:</b> ${data.reply}</p>`;
        }
    </script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML)

@app.route("/chat", methods=["POST"])
def chat():
    user_msg = request.json["message"]
    conversation.append({"role": "user", "content": user_msg})
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=conversation
    )
    reply = response.choices[0].message.content
    conversation.append({"role": "assistant", "content": reply})
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True)