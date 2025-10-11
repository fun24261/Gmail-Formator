from itertools import product
from threading import Thread
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = "8107648163:AAH5pbOD_yjOHdV8yWiN3Zw702bNOl7LmpQ"
MAX_VARIATIONS = 10000  # সর্বোচ্চ Gmail variations

# Dummy Flask server for Render port
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
def generate_gmails(gmail, count):
    username, domain = gmail.split("@")
    variations = []
    letters = [c for c in username]
    for p in product(*[[c.lower(), c.upper()] if c.isalpha() else [c] for c in letters]):
        variations.append("".join(p) + "@" + domain)
        if len(variations) >= count or len(variations) >= MAX_VARIATIONS:
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

# Handle messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    if "@" not in text:
        await update.message.reply_text("Invalid Gmail. আবার চেষ্টা করুন।")
        return

    keyboard = [
        [
            InlineKeyboardButton("100", callback_data=f"{text}|100"),
            InlineKeyboardButton("500", callback_data=f"{text}|500"),
        ],
        [
            InlineKeyboardButton("1000", callback_data=f"{text}|1000"),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("কতটি Gmail variation তৈরি করতে চান?", reply_markup=reply_markup)

# Handle button presses
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    gmail, count = query.data.split("|")
    count = int(count)

    variations = generate_gmails(gmail, count)
    msg = "\n".join(variations)
    remaining = MAX_VARIATIONS - len(variations)

    if remaining > 0:
        msg += f"\n\nআপনি আরও তৈরি করতে পারবেন ({remaining} পর্যন্ত)"
    else:
        msg += "\n\nআর তৈরি করা যাচ্ছে না"

    if len(msg) > 4000:
        msg = "\n".join(variations[:50]) + "\n... (truncated)"
    await query.edit_message_text(f"Generated {len(variations)} Gmail(s):\n{msg}")

# Main function
def main():
    keep_alive()  # Start dummy Flask server

    app_bot = ApplicationBuilder().token(BOT_TOKEN).build()
    app_bot.add_handler(CommandHandler("start", start))
    app_bot.add_handler(CommandHandler("help", start))
    app_bot.add_handler(CallbackQueryHandler(button))
    app_bot.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    print("Bot started successfully!")
    app_bot.run_polling()

if __name__ == "__main__":
    main()
