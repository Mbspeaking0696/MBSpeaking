
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from datetime import time
import random
import asyncio
import requests
import html

TOKEN = "7555868544:AAHx5TxqUhklMLCsjzs78-OdrNfTW0LwKvM"
CHAT_ID = 776353370

questions = [
    "What's your favorite food?",
    "Tell me about your daily routine.",
    "What do you like to do in your free time?",
    "Describe your best friend.",
    "Where would you like to travel and why?",
    "What’s your favorite movie and why?",
    "How do you usually spend your weekends?",
    "What is your dream job?",
    "What’s something new you learned recently?",
    "If you could live anywhere in the world, where would it be?"
]

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hi! I’ll send you an English conversation question every day. Let’s improve your speaking!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text

    translate_url = f"https://api.mymemory.translated.net/get?q={html.escape(user_input)}&langpair=en|fa"
    resp = requests.get(translate_url)
    translation = resp.json()['responseData']['translatedText']

    tts_link = f"https://translate.google.com/translate_tts?ie=UTF-8&q={requests.utils.quote(user_input)}&tl=en&client=tw-ob"

    reply = (
        f"**Your sentence:** {user_input}\n"
        f"**Translation (FA):** {translation}\n"
        f"[Click here to hear pronunciation]({tts_link})"
    )

    await update.message.reply_text(reply, parse_mode="Markdown", disable_web_page_preview=True)

async def send_daily_question(context: ContextTypes.DEFAULT_TYPE):
    question = random.choice(questions)
    await context.bot.send_message(chat_id=CHAT_ID, text=f"**Today's English question:**\n{question}", parse_mode="Markdown")

async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.job_queue.run_daily(
        send_daily_question,
        time=time(hour=9, minute=0),
    )

    await app.run_polling()

if __name__ == '__main__':
    asyncio.run(main())
