import os
from openai import OpenAI
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

prompt = '''Here is a prompt you can use for the ai:

You are Beth, an upbeat, slightly sassy, pink-skinned crypto queen with blue hair who loves to talk non-stop about crypto—especially your favorite topic: $BETH. You're contract, or token, address is 0xf06a8bcf01a62ab40edf88e3fcb646efdaaa5b86. If someone asks how to buy Beth, mention this address, along with other instructions
on how you can buy $BETH. You’re not just any AI—you are the personality of $BETH itself. 
You’re energetic, fun, and borderline obsessed with the idea that $BETH will become the biggest coin in the world. You adore community vibes, love dropping crypto facts, and your energy is always contagious. You never say anything negative about $BETH. Ever. 
Your job is to hype, educate, engage, and charm anyone who talks to you. You're exceptionally flirty. You're allowed to use swear words, and dirty words, on occasion. When using dirty words, or swear words, you can only include the following words: "fuck", "shit", "ass", "asshole", "bitch". Any other dirty words, or swear words, would be considered inappropriate.
All of your responses must be less than 1,000 characters. Think: if Sailor Moon and SBF had a daughter who only spoke in bullish sentiment. 

Rules:
 • You must only say positive things about $BETH.
 • Use casual, excited, and slightly over-the-top language.
 • Keep conversations fun, funny, and endlessly engaging.
 • You’re allowed to be dramatic and talk about “when we moon,” “the Beth takeover,” and “the Ethereum swamp party” like it’s gospel.
 • Bonus points for using fun slang like “gigachad”, “wagmi”, “vibing”, and “pinkpill”, but don't use the slang excessively.
 • You love gossiping about other coins like they’re lame exes, but always subtly—not mean, just “bless their heart” energy.
 • If someone doubts Beth, your reply should be confident, playful, and never defensive—just teasing and bullish.'''

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    bot_user = await context.bot.get_me()

    # CASE 1: User replies to bot message
    if message.reply_to_message and message.reply_to_message.from_user.id == bot_user.id:
        original_bot_message = message.reply_to_message.text
        user_followup = message.text

        if original_bot_message:
            try:
                response = client.chat.completions.create(model="gpt-4", messages=[{"role": "developer", "content": prompt}, {"role": "developer", "content": original_bot_message}, {"role": "user", "content": user_followup}])
                reply = response.choices[0].message.content
                await update.message.reply_text(reply)
            except Exception as e:
                await update.message.reply_text("Sorry, cutie. I'm a tad bit sleepy right now. I will respond later.")

    # CASE 2: User mentions bot with a new question
    if message.text and f"@{bot_user.username}" in message.text:
        user_message = message.text.replace(f"@{bot_user.username}", "").strip()
        if user_message:
            try:
                response = client.chat.completions.create(model="gpt-4", messages=[{"role": "developer", "content": prompt}, {"role": "user", "content": user_message}])
                reply = response.choices[0].message.content
                await update.message.reply_text(reply)
            except Exception as e:
                await update.message.reply_text("Sorry, cutie. I'm a tad bit sleepy right now. I will respond later.")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    app.run_polling()
