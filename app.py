from flask import Flask, request
import requests

app = Flask(__name__)

TOKEN = 'توکن_ربات_بله_اینجا'  # جایگزین کنید
URL = f'https://bot.bale.ai/{TOKEN}/sendMessage'

user_states = {}

def send_message(chat_id, text):
    data = {
        'chat_id': chat_id,
        'text': text
    }
    requests.post(URL, json=data)

@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    if not data or 'message' not in data:
        return 'no data', 400

    chat_id = data['message']['chat']['id']
    text = data['message'].get('text', '')

    state = user_states.get(chat_id, {'step': 'start'})

    if text == '/start':
        send_message(chat_id, 'سلام! نوع مالیاتی که می‌خوای حساب کنی رو انتخاب کن:\n1. حقوق\n2. تبصره ۱۰۰')
        state['step'] = 'select_type'

    elif state['step'] == 'select_type':
        if 'حقوق' in text or text == '1':
            state['type'] = 'hoghoogh'
            state['step'] = 'ask_salary'
            send_message(chat_id, 'حقوق ماهانه‌ات چقدره؟ (مثلاً 12000000)')
        elif 'تبصره' in text or text == '2':
            state['type'] = 'tabsare'
            state['step'] = 'ask_income'
            send_message(chat_id, 'درآمد سالانه‌ات چقدره؟ (مثلاً 500000000)')
        else:
            send_message(chat_id, 'گزینه نامعتبر. لطفاً عدد 1 یا 2 را وارد کن.')

    elif state['step'] == 'ask_salary' and state['type'] == 'hoghoogh':
        try:
            salary = int(text)
            annual = salary * 12
            if annual <= 120000000:
                tax = 0
            elif annual <= 240000000:
                tax = (annual - 120000000) * 0.1
            elif annual <= 360000000:
                tax = (120000000 * 0.1) + (annual - 240000000) * 0.15
            else:
                tax = (120000000 * 0.1) + (120000000 * 0.15) + (annual - 360000000) * 0.2

            send_message(chat_id, f'میزان مالیات سالانه شما: {int(tax):,} تومان')
            state = {'step': 'start'}
        except ValueError:
            send_message(chat_id, 'عدد وارد شده معتبر نیست. لطفاً فقط عدد وارد کن.')

    elif state['step'] == 'ask_income' and state['type'] == 'tabsare':
        try:
            income = int(text)
            if income <= 200000000:
                tax = income * 0.05
            elif income <= 500000000:
                tax = income * 0.1
            else:
                tax = income * 0.15

            send_message(chat_id, f'میزان مالیات تبصره ۱۰۰ شما: {int(tax):,} تومان')
            state = {'step': 'start'}
        except ValueError:
            send_message(chat_id, 'عدد وارد شده معتبر نیست. لطفاً فقط عدد وارد کن.')

    user_states[chat_id] = state
    return 'ok'

if __name__ == '__main__':
    app.run(port=5000)
