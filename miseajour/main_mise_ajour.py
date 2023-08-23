import json
from difflib import get_close_matches
from flask import Flask, request, render_template

app = Flask(__name__, template_folder='template')

# Load the knowledge base from a JSON file
def load_knowledge_base(file_path: str) -> dict:
    with open(file_path, 'r', encoding='utf-8') as file:
        data: dict = json.load(file)
    return data


# Save the updated knowledge base to the JSON file
def save_knowledge_base(file_path: str, data: dict):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)


# Find the closest matching question
def find_best_match(user_question: str, questions: list[str]) -> str | None:
    matches: list = get_close_matches(user_question, questions, n=1, cutoff=0.6)
    return matches[0] if matches else None


def get_answer_for_question(question: str, knowledge_base: dict) -> str | None:
    for q in knowledge_base["questions"]:
        if q["question"] == question:
            answer: str = q["answer"]
            # Replace newline characters with HTML line break tags
            answer = answer.replace('\n', '<br>')
            return answer
    return None


@app.route('/', methods=['GET', 'POST'])
def chatbot():
    knowledge_base: dict = load_knowledge_base('knowledge_base.json')

    if request.method == 'POST':
        user_input: str = request.form['user_input']

        if user_input.lower() == 'خروج':
            return render_template('ChatMates.html', bot_response="مع السلامة")

        best_match: str | None = find_best_match(user_input, [q["question"] for q in knowledge_base["questions"]])

        if best_match:
            answer: str = get_answer_for_question(best_match, knowledge_base) # type: ignore
            return render_template('ChatMates.html', bot_response=answer)
        else:
            return render_template('ChatMates.html', bot_response="I don't know the answer. Can you teach me?")

    return render_template('ChatMates.html', bot_response=None)


if __name__ == "__main__":
    app.run(debug=True)
