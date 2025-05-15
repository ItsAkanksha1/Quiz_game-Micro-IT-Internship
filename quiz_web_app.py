from flask import Flask, render_template, request, session, redirect, url_for
import random
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this for production!

# Load questions once on startup
with open("questions.json", "r", encoding="utf-8") as f:
    ALL_QUESTIONS = json.load(f)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        category = request.form.get("category")
        language = request.form.get("language")
        session["category"] = category
        session["language"] = language

        filtered = ALL_QUESTIONS.get(language, {}).get(category, [])
        questions = filtered[:]
        random.shuffle(questions)
        questions = questions[:10]  # Select 10 questions

        session["questions"] = questions
        session["current"] = 0
        session["score"] = 0

        return redirect(url_for("quiz"))

    categories = ["beginner", "intermediate", "difficult"]
    languages = sorted(ALL_QUESTIONS.keys())
    return render_template("home.html", categories=categories, languages=languages)

@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    questions = session.get("questions", [])
    current_index = session.get("current", 0)

    # If user submitted an answer, handle it here (update score, increment current_index)
    if request.method == "POST":
        selected_answer = request.form.get("answer")
        if selected_answer == questions[current_index]['answer']:
            session["score"] = session.get("score", 0) + 1
        session["current"] = current_index + 1
        current_index = session["current"]

        if current_index >= len(questions):
            return redirect(url_for("result"))

    # Get current question data to show
    if current_index < len(questions):
        current_question_data = questions[current_index]
    else:
        # No more questions, redirect to results
        return redirect(url_for("result"))

    return render_template(
        "quiz.html",
        question=current_question_data['question'],
        options=current_question_data['options'],
        current=current_index + 1,
        total=len(questions)
    )                

@app.route("/result")
def result():
    score = session.get("score", 0)
    total = len(session.get("questions", []))
    return render_template("result.html", score=score, total=total)

if __name__ == "__main__":
    app.run(debug=True)
