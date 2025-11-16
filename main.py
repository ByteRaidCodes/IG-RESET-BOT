from flask import Flask
import asyncio
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from telegram import Update
import os

BOT_TOKEN = os.getenv("7325333749:AAGuciHvW6E0NJg4vlSk4L7jBi2la-oD37A")

app = Flask(__name__)

async def start(update: Update, context):
    await update.message.reply_text("Bot is running!")

async def echo(update: Update, context):
    await update.message.reply_text(update.message.text)

async def run_bot():
    application = (
        ApplicationBuilder()
        .token(BOT_TOKEN)
        .build()
    )

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    await application.initialize()
    await application.start()
    await application.updater.start_polling()
    await application.run_until_disconnected()

@app.route("/")
def home():
    return "Bot is alive!"

if __name__ == "__main__":
    asyncio.run(run_bot())
