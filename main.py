import uuid
import string
import random
import requests
from telegram.ext import Updater, CommandHandler
from flask import Flask
import threading

BOT_TOKEN = "7325333749:AAGuciHvW6E0NJg4vlSk4L7jBi2la-oD37A"

def send_instagram_reset(target):
    if target.startswith("@"):
        return "❌ Enter username without '@'."
    csrf_token = "".join(random.choices(string.ascii_letters + string.digits, k=32))
    if "@" in target:
        data = {
            "_csrftoken": csrf_token,
            "user_email": target,
            "guid": str(uuid.uuid4()),
            "device_id": str(uuid.uuid4())
        }
    else:
        data = {
            "_csrftoken": csrf_token,
            "username": target,
            "guid": str(uuid.uuid4()),
            "device_id": str(uuid.uuid4())
        }
    headers = {
        "user-agent":
            f"Instagram 150.0.0.0.000 Android (29/10; 300dpi; 720x1440; "
            f"{''.join(random.choices(string.ascii_lowercase + string.digits, k=16))}/"
            f"{''.join(random.choices(string.ascii_lowercase + string.digits, k=16))}; "
            f"{''.join(random.choices(string.ascii_lowercase + string.digits, k=16))}; "
            f"{''.join(random.choices(string.ascii_lowercase + string.digits, k=16))}; "
            f"{''.join(random.choices(string.ascii_lowercase + string.digits, k=16))}; en_GB;)"
    }
    response = requests.post(
        "https://i.instagram.com/api/v1/accounts/send_password_reset/",
        headers=headers,
        data=data
    )
    if "obfuscated_email" in response.text:
        return f"✅ Reset email sent!\n\n{response.text}"
    else:
        return f"❌ Failed.\n\n{response.text}"

def reset(update, context):
    try:
        target = context.args[0]
    except:
        update.message.reply_text("Usage: /reset username_or_email")
        return
    update.message.reply_text("⏳ Sending reset request…")
    result = send_instagram_reset(target)
    update.message.reply_text(result)

def main_bot():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("reset", reset))
    updater.start_polling()
    print("BOT IS RUNNING…")
    updater.idle()

app = Flask("")

@app.route("/")
def home():
    return "Bot is online."

def run_web():
    app.run(host="0.0.0.0", port=8080)

if __name__ == "__main__":
    threading.Thread(target=run_web).start()
    main_bot()
