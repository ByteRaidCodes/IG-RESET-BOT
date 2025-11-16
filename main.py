import uuid
import string
import random
import requests
from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = "7325333749:AAGuciHvW6E0NJg4vlSk4L7jBi2la-oD37A"


# ------------ INSTAGRAM RESET ------------
def send_instagram_reset(target):
    if target.startswith("@"):
        return "❌ Enter username without '@'."

    if "@" in target:
        data = {
            "_csrftoken": "".join(random.choices(string.ascii_letters + string.digits, k=32)),
            "user_email": target,
            "guid": str(uuid.uuid4()),
            "device_id": str(uuid.uuid4())
        }
    else:
        data = {
            "_csrftoken": "".join(random.choices(string.ascii_letters + string.digits, k=32)),
            "username": target,
            "guid": str(uuid.uuid4()),
            "device_id": str(uuid.uuid4())
        }

    headers = {
        "user-agent": "Instagram 150.0.0.0.000 Android"
    }

    r = requests.post(
        "https://i.instagram.com/api/v1/accounts/send_password_reset/",
        headers=headers,
        data=data
    )

    if "obfuscated_email" in r.text:
        return "✅ Reset link sent!\n\n" + r.text
    else:
        return "❌ Failed.\n\n" + r.text


# ------------ TELEGRAM COMMAND ------------
async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /reset username_or_email")
        return

    target = context.args[0]
    await update.message.reply_text("⏳ Sending reset request...")

    result = send_instagram_reset(target)
    await update.message.reply_text(result)


# ------------ TELEGRAM BOT START ------------
async def start_bot():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("reset", reset))

    print("BOT RUNNING...")
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    await app.updater.idle()


# ------------ FLASK WEB SERVER FOR RAILWAY ------------
flask_app = Flask(__name__)

@flask_app.route("/")
def home():
    return "Bot is alive."

def run_server():
    flask_app.run(host="0.0.0.0", port=8080)


# ------------ ENTRY POINT ------------
if __name__ == "__main__":
    Thread(target=run_server).start()

    import asyncio
    asyncio.run(start_bot())
