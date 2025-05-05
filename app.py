from flask import Flask, request, jsonify
import json

app = Flask(__name__)

# تابع ارسال پیام به کاربر
def send_message(user_id, message):
    url = f'https://api.bale.ai/bot{your_bot_token}/sendMessage'
    headers = {'Content-Type': 'application/json'}
    payload = {
        'user_id': user_id,
        'text': message
    }
    response = requests.post(url, json=payload, headers=headers)
    return response

# تابع محاسبه مالیات حقوق
def calculate_tax_income(income):
    if income <= 24000000:
        return 0
    elif income <= 72000000:
        return (income - 24000000) * 0.1
    elif income <= 120000000:
        return (income - 72000000) * 0.2 + 4800000
    elif income <= 180000000:
        return (income - 120000000) * 0.3 + 14400000
    else:
        return (income - 180000000) * 0.4 + 32400000

# تابع محاسبه مالیات تبصره 100
def calculate_tax_tab_100(sales):
    # اینجا به‌صورت فرضی 5 درصد مالیات در نظر گرفته شده است
    return sales * 0.05

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()

    # چاپ داده‌های دریافتی برای بررسی ساختار آنها
    print(data)

    if 'message' in data:
        message_text = data['message']['text']
        user_id = data['message']['user_id']  # استفاده از user_id به جای author_object_id

        if message_text.lower() == 'شروع':
            send_message(user_id, "چه نوع مالیاتی می‌خواهید محاسبه کنید؟\n1. مالیات حقوق\n2. مالیات تبصره 100")

        elif message_text == '1':
            send_message(user_id, "لطفا مبلغ حقوق خود را وارد کنید:")

        elif message_text == '2':
            send_message(user_id, "لطفا مبلغ فروش خود را وارد کنید:")

        elif message_text.isdigit():
            amount = int(message_text)
            if amount <= 24000000:
                send_message(user_id, "مبلغ وارد شده معاف از مالیات است.")
            else:
                if message_text == '1':
                    tax = calculate_tax_income(amount)
                    send_message(user_id, f"مالیات شما به مبلغ {amount:,} تومان برابر با {tax:,} تومان خواهد بود.")
                elif message_text == '2':
                    tax = calculate_tax_tab_100(amount)
                    send_message(user_id, f"مالیات شما از فروش به مبلغ {amount:,} تومان برابر با {tax:,} تومان خواهد بود.")

        else:
            send_message(user_id, "لطفا مبلغ را به درستی وارد کنید.")

    return jsonify({'status': 'ok'}), 200

if __name__ == '__main__':
    app.run(debug=True)
