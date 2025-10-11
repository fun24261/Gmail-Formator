from itertools import product
from threading import Thread
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = "8107648163:AAH5pbOD_yjOHdV8yWiN3Zw702bNOl7LmpQ"
MAX_VARIATIONS = 10000
CHUNK_FIRST = 100  # প্রথমে generate করা Gmail সংখ্যা

# Dummy Flask server (Free Plan compatibility)
flask_app = Flask("")

@flask_app.route("/")
def home():
    return "Bot is running!"

def run_flask():
    flask_app.run(host="0.0.0.0", port=5000)

def keep_alive():
    t = Thread(target=run_flask)
    t.start()

# Gmail generator
def generate_gmails(gmail):
    username, domain = gmail.split("@")
    variations = []
    letters = [c for c in username]
    for p in product(*[[c.lower(), c.upper()] if c.isalpha() else [c] for c in letters]):
        variations.append("".join(p) + "@" + domain)
        if len(variations) >= MAX_VARIATIONS:
            break
    return variations

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "আপনাকে স্বাগতম\n"
        "আপনি একটা gmail দিয়েই আনলিমিটেড জিমেইল তৈরি করতে পারবেন\n"
        "দয়া করে আমাকে জিমেইল সেন্ড করুন"
    )
    await update.message.reply_text(welcome_text)

# Helper to send long messages in chunks
async def send_long_message(chat_id, text, context):
    chunk_size = 4000
    for i in range(0, len(text), chunk_size):
        await context.bot.send_message(chat_id, text[i:i+chunk_size])

# Handle Gmail messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    gmail = update.message.text.strip()
    if "@" not in gmail:
        await update.message.reply_text("Invalid Gmail. আবার চেষ্টা করুন।")
        return

    variations = generate_gmails(gmail)
    first_chunk = variations[:CHUNK_FIRST]
    remaining = variations[CHUNK_FIRST:]

    msg = "\n".join(first_chunk)
    await send_long_message(update.message.chat_id, msg, context)

    if remaining:
        keyboard = [[InlineKeyboardButton("আরো তৈরি করুন", callback_data=gmail)]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("আরো Gmail variations generate করতে নিচের বাটন চাপুন:", reply_markup=reply_markup)
    else:
        await update.message.reply_text("আর তৈরি করা যাচ্ছে না")

# Handle "আরো তৈরি করুন" button
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    gmail = query.data
    variations = generate_gmails(gmail)
    first_chunk = variations[:CHUNK_FIRST]
    remaining = variations[CHUNK_FIRST:]

    msg = "\n".join(remaining)
    if msg:
        await send_long_message(query.message.chat_id, msg, context)
        await query.edit_message_text("সব Gmail variations পাঠানো হয়েছে")
    else:
        await query.edit_message_text("আর তৈরি করা যাচ্ছে না")

# Main function
def main():
    keep_alive()  # Start dummy Flask server for Render Free Plan

    app_bot = ApplicationBuilder().token(BOT_TOKEN).build()
    app_bot.add_handler(CommandHandler("start", start))
    app_bot.add_handler(CommandHandler("help", start))
    app_bot.add_handler(CallbackQueryHandler(button))
    app_bot.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    print("Bot started successfully!")
    app_bot.run_polling()

if __name__ == "__main__":
    main()
