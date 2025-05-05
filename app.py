
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# توکن بوت بله خود را در اینجا وارد کنید
TOKEN = "توکن_ربات_شما"
WEBHOOK_URL = "https://bale-tax-bot.onrender.com/webhook"  # آدرس webhook ربات

# معافیت ماهانه 24 میلیون تومان
TAX_FREE_THRESHOLD = 24000000

def calculate_tax_income(income):
    """محاسبه مالیات برای درآمد حقوق طبق قوانین 1404"""
    tax = 0
    
    if income <= TAX_FREE_THRESHOLD:
        return tax  # معاف از مالیات
    
    # برای درآمدهای بیشتر از 24 میلیون تومان
    if income <= 30000000:
        # 10% مالیات برای درآمد 24 تا 30 میلیون
        tax = (income - TAX_FREE_THRESHOLD) * 0.10  
    elif income <= 38000000:
        # 15% مالیات برای درآمد 30 تا 38 میلیون
        tax = (income - 30000000) * 0.15 + (30000000 - TAX_FREE_THRESHOLD) * 0.10  
    elif income <= 50000000:
        # 20% مالیات برای درآمد 38 تا 50 میلیون
        tax = (income - 38000000) * 0.20 + (38000000 - 30000000) * 0.15 + (30000000 - TAX_FREE_THRESHOLD) * 0.10  
    elif income <= 66667000:
        # 25% مالیات برای درآمد 50 تا 66.67 میلیون
        tax = (income - 50000000) * 0.25 + (50000000 - 38000000) * 0.20 + (38000000 - 30000000) * 0.15 + (30000000 - TAX_FREE_THRESHOLD) * 0.10  
    else:
        # 30% مالیات برای درآمد بیشتر از 66.67 میلیون
        tax = (income - 66667000) * 0.30 + (66667000 - 50000000) * 0.25 + (50000000 - 38000000) * 0.20 + (38000000 - 30000000) * 0.15 + (30000000 - TAX_FREE_THRESHOLD) * 0.10

    return tax

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()

    if 'message' in data:
        message_text = data['message']['text']
        user_id = data['message']['author_object_id']
        
        # اگر اولین پیام باشد، از کاربر بپرسیم که مالیات حقوق می‌خواهد یا تبصره 100
        if message_text.lower() == 'شروع':
            send_message(user_id, "چه نوع مالیاتی می‌خواهید محاسبه کنید؟\n1. مالیات حقوق\n2. مالیات تبصره 100")
        
        # اگر کاربر گزینه مالیات حقوق را انتخاب کند
        elif message_text == '1':
            send_message(user_id, "لطفا مبلغ حقوق خود را وارد کنید:")
            # ذخیره وضعیت برای محاسبه مالیات حقوق
            # این کار را می‌توانید در دیتابیس یا متغیرهای موقت انجام دهید

        # اگر کاربر گزینه مالیات تبصره 100 را انتخاب کند
        elif message_text == '2':
            send_message(user_id, "لطفا مبلغ فروش خود را وارد کنید:")
            # ذخیره وضعیت برای محاسبه مالیات تبصره 100

        # بررسی اینکه آیا ورودی، مبلغ حقوق است
        elif message_text.isdigit():
            income = int(message_text)
            # در اینجا باید وضعیت مالیاتی را بررسی کنیم که آیا مالیات حقوق است یا تبصره 100
            # فرض کنیم که اگر انتخاب شده باشد، مالیات حقوق باشد:
            tax = calculate_tax_income(income)
            send_message(user_id, f"مالیات شما به مبلغ {income:,} تومان برابر با {tax:,} تومان خواهد بود.")
        
        else:
            send_message(user_id, "لطفا مبلغ را به درستی وارد کنید.")

    return jsonify({'status': 'ok'}), 200

def send_message(user_id, message):
    """ارسال پیام به کاربر"""
    url = f"https://api.bale.ai/bot/{TOKEN}/sendMessage"
    payload = {
        'user_id': user_id,
        'text': message
    }
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.json()

if __name__ == '__main__':
    app.run(debug=True)
