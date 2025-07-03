# telegram_bot.py

from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import requests

# === CLI chatbot logic එක 그대로 retain කරනවා ===

API_KEY = "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"
API_URL = "https://openrouter.ai/api/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# Shared message history
messages = [
    {"role": "system", "content": "My name is Sithum. I'm a helpful Sinhala-English speaking assistant who loves trivia and fun conversations."}
]

def chat_with_bot(user_input):
    messages.append({"role": "user", "content": user_input})

    data = {
        "model": "deepseek/deepseek-r1:free",
        "messages": messages
    }

    try:
        response = requests.post(API_URL, headers=headers, json=data)
        response.raise_for_status()
        response_json = response.json()

        if "choices" in response_json:
            reply = response_json["choices"][0]["message"]["content"]
            messages.append({"role": "assistant", "content": reply})
            return reply.strip()
        else:
            return "❌ Unexpected response from API."

    except requests.exceptions.RequestException as e:
        return f"❌ API call failed: {e}"

# === Telegram bot logic ===

TELEGRAM_BOT_TOKEN = "7804359849:AAEdNlanzWeIoWSWcSqNy6NlHQFfIN6opt8"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    reply = chat_with_bot(user_input)
    await update.message.reply_text(reply)

if __name__ == "__main__":
    print("🤖 Telegram bot is running... Press Ctrl+C to stop.")
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
