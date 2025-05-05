
from flask import Flask, request
import requests

app = Flask(__name__)

# توکن رباتت رو اینجا بذار
TOKEN = '4303010:qOeO6azOv5o1ej4IEZEdE6HB5nnn3YFe25gBjibY'
BALE_API_URL = f'https://tapi.bale.ai/bot{TOKEN}/sendMessage'

@app.route('/')
def home():
    return 'ربات بله فعال است.'

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    print("داده دریافتی:", data)

    if 'message' in data:
        message = data['message']
        user_id = message.get('author_object_id') or message.get('chat', {}).get('id')
        text = message.get('text', '')

        if text.strip() == 'شروع':
            send_message(user_id, 'سلام! به ربات محاسبه مالیات تبصره ۱۰۰ خوش آمدید.')

    return '', 200

def send_message(chat_id, text):
    payload = {
        'chat_id': chat_id,
        'text': text
    }
    response = requests.post(BALE_API_URL, json=payload)
    print("پاسخ ارسال پیام:", response.status_code, response.text)
