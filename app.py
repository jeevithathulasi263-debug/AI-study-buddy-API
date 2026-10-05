from flask import Flask, request, render_template_string
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY not found in .env file")

client = Groq(api_key=api_key)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>AI StudyBuddy</title>
</head>
<body>

    <h1>AI StudyBuddy 📚</h1>

    <form method="POST">
        <textarea name="question" rows="5" cols="60"
        placeholder="Ask your study question..."></textarea>
        <br><br>
        <button type="submit">Ask AI</button>
    </form>

    {% if answer %}
        <h2>Answer:</h2>
        <p>{{ answer }}</p>
    {% endif %}

</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():

    answer = ""

    if request.method == "POST":

        question = request.form.get("question")

        if question:

            try:
                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a helpful AI StudyBuddy. Explain answers simply for students."
                        },
                        {
                            "role": "user",
                            "content": question
                        }
                    ]
                )

                answer = response.choices[0].message.content

            except Exception as e:
                answer = "Error: " + str(e)

    return render_template_string(HTML, answer=answer)


if __name__ == "__main__":
    app.run(debug=False, use_reloader=False)