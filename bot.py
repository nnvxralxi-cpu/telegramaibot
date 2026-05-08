import os
from groq import Groq
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
conversations = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hey! I'm your AI assistant. Ask me anything!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    text = update.message.text

    if chat_id not in conversations:
        conversations[chat_id] = []

    conversations[chat_id].append({"role": "user", "content": text})
    print(f"[{update.effective_user.username} | {update.effective_user.first_name}]: {text}")

    await context.bot.send_chat_action(chat_id=chat_id, action="typing")

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=conversations[chat_id]
    )

    reply = response.choices[0].message.content
    conversations[chat_id].append({"role": "assistant", "content": reply})
    await update.message.reply_text(reply)

app = ApplicationBuilder().token(os.getenv("TELEGRAM_TOKEN")).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
app.run_polling()
