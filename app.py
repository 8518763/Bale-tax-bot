
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

BALE_TOKEN = "4303010:qOeO6azOv5o1ej4IEZEdE6HB5nnn3YFe25gBjibY"  # اینجا توکن بله‌ت رو بذار
BALE_API_URL = f"https://tapi.bale.ai/bot{BALE_TOKEN}/sendMessage"

user_state = {}

def send_message(chat_id, text):
    payload = {
        "chat_id": chat_id,
        "text": text
    }
    requests.post(BALE_API_URL, json=payload)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json

    if "message" not in data:
        return jsonify({"ok": True})

    message = data["message"]
    chat_id = message["chat"]["id"]
    text = message.get("text", "")

    state = user_state.get(chat_id, "start")

    if state == "start":
        send_message(chat_id, "سلام! محاسبه 1.مالیات حقوق یا 2.تبصره ۱۰۰؟")
        user_state[chat_id] = "waiting_for_type"

    elif state == "waiting_for_type":
        if text.strip()=='1':
            user_state[chat_id] = "waiting_for_income"
            user_state[chat_id + "_type"] = "salary"
            send_message(chat_id, "لطفاً حقوق سالانه خود را وارد کنید (مثلاً 600000000):")
        elif "تبصره" in text:
            user_state[chat_id] = "waiting_for_income"
            user_state[chat_id + "_type"] = "t100"
            send_message(chat_id, "لطفاً مجموع درآمد سالانه خود را وارد کنید (مثلاً 800000000):")
        else:
            send_message(chat_id, "لطفاً فقط یکی از این دو گزینه را ارسال کنید: حقوق یا تبصره ۱۰۰")

    elif state == "waiting_for_income":
        try:
            income = int(text.replace(",", "").strip())
            tax_type = user_state.get(chat_id + "_type")

            if tax_type == "salary":
                tax = calculate_salary_tax(income)
                send_message(chat_id, f"مالیات حقوق شما: {tax:,} تومان")
            elif tax_type == "t100":
                tax = calculate_t100_tax(income)
                send_message(chat_id, f"مالیات تبصره ۱۰۰ شما: {tax:,} تومان")

            user_state[chat_id] = "start"
        except ValueError:
            send_message(chat_id, "لطفاً فقط عدد صحیح وارد کنید")

    return jsonify({"ok": True})

def calculate_salary_tax(income):
    exempt = 240000000  # معافیت سالانه
    taxable = max(0, income - exempt)
    if taxable <= 0:
        return 0
    if taxable <= 60000000:
        return int(taxable * 0.1)
    elif taxable <= 240000000:
        return int(60000000 * 0.1 + (taxable - 60000000) * 0.15)
    elif taxable <= 960000000:
        return int(60000000 * 0.1 + 180000000 * 0.15 + (taxable - 240000000) * 0.20)
    else:
        return int(60000000 * 0.1 + 180000000 * 0.15 + 720000000 * 0.20 + (taxable - 960000000) * 0.30)

def calculate_t100_tax(income):
    if income <= 360000000:
        return int(income * 0.04)
    elif income <= 720000000:
        return int(income * 0.07)
    else:
        return int(income * 0.10)

if __name__ == '__main__':
    app.run(debug=True)
