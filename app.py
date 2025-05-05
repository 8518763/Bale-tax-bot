
from flask import Flask, request
import requests

app = Flask(__name__)

TOKEN = '4303010:qOeO6azOv5o1ej4IEZEdE6HB5nnn3YFe25gBjibY'
URL = f'https://api.telegram.org/bot{TOKEN}/sendMessage'

user_states = {}

def calculate_tax_1404(income):
    annual_income = income * 12
    if annual_income <= 288000000:
        return 0
    elif annual_income <= 1200000000:
        return (annual_income - 288000000) * 0.10
    elif annual_income <= 2520000000:
        return (1200000000 - 288000000) * 0.10 + (annual_income - 1200000000) * 0.15
    elif annual_income <= 4200000000:
        return (1200000000 - 288000000) * 0.10 + (2520000000 - 1200000000) * 0.15 + (annual_income - 2520000000) * 0.20
    else:
        return (1200000000 - 288000000) * 0.10 + (2520000000 - 1200000000) * 0.15 + (4200000000 - 2520000000) * 0.20 + (annual_income - 4200000000) * 0.30

def calculate_tafsare100_tax(income):
    if income <= 480000000:
        return income * 0.05
    elif income <= 1000000000:
        return income * 0.10
    elif income <= 2000000000:
        return income * 0.15
    else:
        return income * 0.20

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    if 'message' not in data or 'text' not in data['message']:
        return 'ok'

    chat_id = data['message']['chat']['id']
    text = data['message']['text']
    state = user_states.get(chat_id, 'start')

    if state == 'start':
        user_states[chat_id] = 'choose_type'
        send_message(chat_id, "سلام! محاسبه کدام نوع مالیات را می‌خواهید؟\n1. مالیات حقوق\n2. تبصره ۱۰۰\nلطفاً عدد 1 یا 2 را وارد کنید.")
    elif state == 'choose_type':
        if text == '1':
            user_states[chat_id] = 'await_salary'
            send_message(chat_id, "لطفاً حقوق ماهیانه خود را به تومان وارد کنید:")
        elif text == '2':
            user_states[chat_id] = 'await_income'
            send_message(chat_id, "لطفاً درآمد سالانه خود را به تومان وارد کنید:")
        else:
            send_message(chat_id, "ورودی نامعتبر است. لطفاً فقط عدد 1 یا 2 را وارد کنید.")
    elif state == 'await_salary':
        try:
            income = int(text)
            tax = calculate_tax_1404(income)
            send_message(chat_id, f"میزان مالیات سال ۱۴۰۴ شما برابر است با: {int(tax):,} تومان")
            user_states[chat_id] = 'start'
        except:
            send_message(chat_id, "لطفاً یک عدد معتبر وارد کنید.")
    elif state == 'await_income':
        try:
            income = int(text)
            tax = calculate_tafsare100_tax(income)
            send_message(chat_id, f"میزان مالیات تبصره ۱۰۰ شما برابر است با: {int(tax):,} تومان")
            user_states[chat_id] = 'start'
        except:
            send_message(chat_id, "لطفاً یک عدد معتبر وارد کنید.")

    return 'ok'

def send_message(chat_id, text):
    payload = {
        'chat_id': chat_id,
        'text': text
    }
    requests.post(URL, json=payload)

if __name__ == '__main__':
    app.run(debug=True)
