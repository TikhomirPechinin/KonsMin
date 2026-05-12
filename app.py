import os
import json
import requests
from flask import Flask, request
from dotenv import load_dotenv
from yandex_ai_studio_sdk import AIStudio

load_dotenv()

app = Flask(__name__)

VK_ACCESS_TOKEN = os.getenv('VK_ACCESS_TOKEN')
CONFIRMATION_STRING = os.getenv('CONFIRMATION_STRING')
YANDEX_FOLDER_ID = os.getenv('YANDEX_FOLDER_ID')
YANDEX_API_KEY = os.getenv('YANDEX_API_KEY')

sdk = AIStudio(folder_id=YANDEX_FOLDER_ID, auth=YANDEX_API_KEY)

def send_vk_message(user_id, message):
    url = 'https://api.vk.com/method/messages.send'
    params = {
        'user_id': user_id,
        'message': message,
        'access_token': VK_ACCESS_TOKEN,
        'v': '5.199',
        'random_id': 0
    }
    requests.get(url, params=params)

def ask_yandexgpt(question):
    try:
        model = sdk.models.completions('yandexgpt-lite')
        model = model.configure(temperature=0.6, max_tokens=500)
        result = model.run([
            {"role": "system", "text": "Ты консультант профсоюза студентов ХГУ. Отвечай кратко и дружелюбно."},
            {"role": "user", "text": question}
        ])
        return result[0].text if result else "Не удалось получить ответ."
    except Exception as e:
        return f"Ошибка: {str(e)}"

@app.route('/')
def index():
    return "Consultant is running"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    if data.get('type') == 'confirmation':
        return CONFIRMATION_STRING
    
    if data.get('type') == 'message_new':
        user_id = data['object']['message']['from_id']
        user_text = data['object']['message'].get('text', '').strip()
        
        answer = ask_yandexgpt(user_text)
        send_vk_message(user_id, answer)
    
    return 'ok'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=False)