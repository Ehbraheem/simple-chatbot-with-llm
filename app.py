import json

from flask import Flask, request
from flask_cors import CORS

from bot import respond_to_prompt

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return 'Hello, World!'


# Request shape
# {
#     'prompt': 'message'
# }

@app.route('/chatbot', methods=['POST'])
def handle_prompt():
    data = request.get_data(as_text=True)
    data = json.loads(data)
    input_text = data['prompt']

    response = respond_to_prompt(input_text)

    return response




if __name__ == '__main__':
    app.run()
