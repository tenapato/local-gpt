from flask import Flask, request
from flask.json import jsonify
import openai
import os
from dotenv import load_dotenv


# Load the environment variables from the .env file
# load_dotenv(os.environ.get("DOTENV_PATH"))

# openai.api_key = os.getenv("OPEN_AI_KEY")
openai.api_key = os.environ.get("OPEN_AI_KEY") 

# Set this to `True` if you need GPT4. If not, the code will use GPT-3.5.
#GPT4 = False

GPT4 = False

class Conversation:
    messages = None

    def __init__(self):
        Conversation.messages = [
            {
                "role": "system",
                "content": (
                    "When asked for code, you don't explain it unless specifically asked to. "
                    "You are a helpful, intelligent, software engineer assistant. "
                    "Answer the user prompt concisely, and avoid additional comments "
                    "other than the code itself, don't explain the code!"
                ),
            }
        ]

    def answer(self, prompt, use_gpt4):
        self._update("user", prompt)

        model = "gpt-4-0613" if use_gpt4 else "gpt-3.5-turbo-0613"
        print(f"Using model: {model}")

        response = openai.ChatCompletion.create(
            model=model,
            messages=Conversation.messages,
            temperature=0,
        )

        self._update("assistant", response.choices[0].message.content)

        return response.choices[0].message.content

    def reset(self):
        Conversation.messages = []

    def _update(self, role, content):
        Conversation.messages.append({
            "role": role,
            "content": content,
        })

        if len(Conversation.messages) > 20:
            Conversation.messages.pop(0)


app = Flask(__name__)
conversation = Conversation()


@app.route("/api/answer", methods=["POST"])
def answer_prompt():
    prompt = request.json.get("prompt")
    use_gpt4 = request.args.get("gpt4", default=str(GPT4)).lower() == "true"
    if prompt:
        answer = conversation.answer(prompt, use_gpt4)
        return answer
    else:
        return jsonify({"error": "Invalid request"}), 400


@app.route("/api/reset", methods=["POST"])
def reset_conversation():
    conversation.reset()
    return jsonify({"message": "Conversation reset"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5002))
    app.run(host='0.0.0.0', port=port)
