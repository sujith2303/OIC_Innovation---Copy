from flask import Flask, render_template, request, jsonify
# from generate_text import generate_text
from main import response_generator



def generate_text(user_input):
    chat_history  = ''
    response =response_generator(user_input,chat_history)
    print(response)
    # chat_history += f"""User: {prompt}\nBot: {response}\n"""
    return response

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    response = generate_text(user_input)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
