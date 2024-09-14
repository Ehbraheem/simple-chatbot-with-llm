from functools import reduce
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from utils import get_db_connection

model_name = "facebook/blenderbot-400M-distill"

model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

def get_chat_history(user_id = None): 
    db = get_db_connection()
    chats = db.execute('SELECT prompt, response from chats order by created_at asc').fetchall()
    history = flattend_history(chats)

    return history

def respond_to_prompt(input_text):
    history_string = get_chat_history()
    inputs = tokenizer.encode_plus(history_string, input_text, return_tensors='pt')

    outputs = model.generate(**inputs)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True).strip()
    db = get_db_connection()
    db.execute('INSERT INTO chats (prompt, response) VALUES (?, ?)', (input_text, response))
    db.commit()

    return response


def flattend_history(rows):
    flat = reduce(lambda accum, curr: '\n'.join([accum, *curr]), rows, '')

    return flat

if __name__ == '__main__':
    while True:
        input_text = input('> ')

        response = respond_to_prompt(input_text)
        print(response)