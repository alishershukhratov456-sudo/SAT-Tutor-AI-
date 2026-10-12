
import os

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request
from google import genai

load_dotenv()

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json(silent=True) or {}
    question = data.get("question", "").strip()
    section = data.get("section", "Math")

    if not question:
        return jsonify({"error": "Please enter a question."}), 400

    if section not in ("Math", "Reading & Writing"):
        return jsonify({"error": "Invalid SAT section."}), 400

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return jsonify({
            "error": "Gemini API key missing. Check your .env file."
        }), 503

    prompt = f"""
You are SAT Tutor AI, a friendly and accurate SAT tutor.

SAT section: {section}
Student's question: {question}

Instructions:
- Explain the solution clearly, step by step.
- Use simple, student-friendly language.
- For Math, show calculations using plain text.
- For Reading & Writing, explain grammar, vocabulary,
  evidence, and reasoning as appropriate.
- For multiple-choice questions, explain the correct
  answer and briefly explain why other options are wrong.
- If the question is unclear, ask for clarification.
- Never invent information.

FORMATTING RULES — IMPORTANT:
- Use plain text only.
- Do not use Markdown formatting.
- Do not use #, ##, **, __, backticks, or decorative symbols.
- Do not wrap equations in dollar signs.
- Do not use percent signs unless a percentage is part
  of the actual question or mathematical answer.
- Write headings as ordinary words, without symbols.
- Use numbered steps like "Step 1:" and "Step 2:".
- Write fractions as "1/2" and multiplication as "×".
- Keep the answer readable and well organized.
"""

    try:
        client = genai.Client(api_key=api_key)

        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=prompt,
        )

        answer = response.text

        if not answer:
            return jsonify({
                "error": "The AI returned an empty answer. Please retry."
            }), 502

        return jsonify({"answer": answer})

    except Exception:
        app.logger.exception("Gemini request failed")
        return jsonify({
            "error": (
                "The AI request failed. Check your API key, "
                "internet connection, and Gemini API quota."
            )
        }), 502


if __name__ == "__main__":
    app.run(debug=True)