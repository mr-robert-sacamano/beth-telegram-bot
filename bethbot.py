import os
from openai import OpenAI
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    if not user_message:
        return

    try:
        response = client.chat.completions.create(model="gpt-4",
        messages=[{"role": "user", "content": user_message}])
        reply = response.choices[0].message.content
        await update.message.reply_text(reply)
    except Exception as e:
        await update.message.reply_text(f"OpenAI error: {e}")
        #await update.message.reply_text("Error communicating with OpenAI.")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    app.run_polling()
