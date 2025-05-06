from flask import Flask, request
import requests

app = Flask(__name__)

TOKEN = '4303010:qOeO6azOv5o1ej4IEZEdE6HB5nnn3YFe25gBjibY'
BALE_API_URL = f'https://tapi.bale.ai/bot{TOKEN}/sendMessage'

@app.route('/')
def home():
    return 'ربات بله فعال است.'
    


@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    if not data or 'message' not in data:
        return 'no data', 400

    chat_id = data['message']['chat']['id']
    text = data['message'].get('text', '')

    state = user_states.get(chat_id, {'step': 'start'})

    
    if 'message' in data:
        message = data['message']
        user_id = message.get('author_object_id') or message.get('chat', {}).get('id')
        text = message.get('text', '')

        if text.strip() == '/start':
            send_message(user_id, 'آیا می‌خواهید مالیات حقوق یا مالیات تبصره 100 رو محاسبه کنید؟\n1. مالیات حقوق\n2. مالیات تبصره 100')
        
        elif text.strip() == '1':  # مالیات حقوق
            send_message(user_id, 'لطفاً درآمد خود را وارد کنید:')
        
        elif text.strip() == '2':  # مالیات تبصره 100
            send_message(user_id, 'لطفاً شغل و درآمد خود را وارد کنید تا محاسبه انجام شود.')
        else:
            send_message(user_id, 'لطفاً فقط یکی از این دو گزینه را ارسال کنید: حقوق یا تبصره ۱۰۰')

    return '', 200

def send_message(chat_id, text):
    payload = {
        'chat_id': chat_id,
        'text': text
    }
    response = requests.post(BALE_API_URL, json=payload)
    print("پاسخ ارسال پیام:", response.status_code, response.text)
