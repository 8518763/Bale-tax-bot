from flask import Flask, request, jsonify

app = Flask(__name__)

user_sessions = {}

tax_rates = {
    "گروه اول": 0.15,
    "گروه دوم": 0.10,
    "گروه سوم": 0.07,
    "گروه چهارم": 0.05
}
exemption_zones = {
    "عادی": 0,
    "محروم": 0.5
}

@app.route('/', methods=['GET'])
def index():
    return 'Hello from Bale bot!'

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    user_id = data['message']['author_object_id']
    text = data['message']['text'].strip()

    session = user_sessions.get(user_id, {"step": 0})

    if text.lower() in ["/start", "شروع", "سلام"]:
        user_sessions[user_id] = {"step": 1}
        reply = "سلام! لطفاً گروه شغلی خود را وارد کنید (گروه اول، دوم، سوم، چهارم)"
    
    elif session["step"] == 1:
        if text in tax_rates:
            session["group"] = text
            session["step"] = 2
            reply = "درآمد سالانه خود را به تومان وارد کنید (مثلاً: 250000000)"
        else:
            reply = "لطفاً یکی از گروه‌های شغلی معتبر را وارد کنید (گروه اول تا چهارم)"
    
    elif session["step"] == 2:
        try:
            income = int(text.replace(",", ""))
            session["income"] = income
            session["step"] = 3
            reply = "آیا در منطقه محروم فعالیت دارید؟ (بله / خیر)"
        except:
            reply = "درآمد باید عددی باشد. لطفاً مجدد وارد کنید."
    
    elif session["step"] == 3:
        if text in ["بله", "بلی", "آره"]:
            session["zone"] = "محروم"
        else:
            session["zone"] = "عادی"

        group = session["group"]
        income = session["income"]
        zone = session["zone"]

        rate = tax_rates[group]
        discount = exemption_zones[zone]
        final_tax = income * rate * (1 - discount)

        reply = (
            f"محاسبه نهایی:"
            f"گروه شغلی: {group}"
            f"درآمد سالانه: {income:,.0f} تومان"
            f"منطقه: {zone}"
            f"نرخ مالیات: {int(rate * 100)}٪"
            f"معافیت منطقه‌ای: {int(discount * 100)}٪"
            f"مالیات قابل پرداخت: {final_tax:,.0f} تومان"
            "برای شروع دوباره بنویس: شروع"
        )
        session["step"] = 0

    else:
        reply = "برای شروع بنویس: شروع"

    user_sessions[user_id] = session

    return jsonify({
        "recipient": {"type": "User", "id": user_id},
        "message": {"type": "Text", "text": reply}
    })

if __name__ == '__main__':
    app.run()
