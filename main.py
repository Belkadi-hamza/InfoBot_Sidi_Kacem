import json
from difflib import get_close_matches
from flask import Flask, request, render_template

app = Flask(__name__, template_folder='template')

# Load the knowledge base from a JSON file
def load_knowledge_base(file_path: str) -> dict:
    with open(file_path, 'r', encoding='utf-8') as file:
        data: dict = json.load(file)
    return data

def find_best_match(user_question: str, questions: list[str]) -> str | None:
    matches: list = get_close_matches(user_question, questions, n=1, cutoff=0.6)
    return matches[0] if matches else None

def get_answer_for_question(question: str, knowledge_base: dict) -> str | None:
    for q in knowledge_base["questions"]:
        if q["question"] == question:
            answer: str = q["answer"]
            answer = answer.replace('\n', '<br>')
            return answer
    return None

def chatbot_response(user_input: str, knowledge_base: dict) -> str:
    if user_input.lower() == 'خروج':
        return "مع السلامة"

    best_match = find_best_match(user_input, [q["question"] for q in knowledge_base["questions"]])

    if best_match:
        answer = get_answer_for_question(best_match, knowledge_base)
        return answer # type: ignore
    else:
        return "عذرًا، لا أعرف الإجابة على هذا السؤال."

@app.route('/', methods=['GET', 'POST'])
def chatbot():
    knowledge_base = load_knowledge_base('knowledge_base.json')

    if request.method == 'POST':
        user_input = request.form['user_input']

        response = chatbot_response(user_input, knowledge_base)
        if not response:
            response = "عذرًا، لا أعرف الإجابة على هذا السؤال."
        
        return render_template('InfoBot.html', bot_response=response)

    return render_template('InfoBot.html', bot_response=None)

if __name__ == "__main__":
    app.run(debug=True)
