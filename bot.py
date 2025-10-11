import os
from flask import Flask
from threading import Thread
from itertools import product
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = "8107648163:AAH5pbOD_yjOHdV8yWiN3Zw702bNOl7LmpQ"

# Flask dummy server to satisfy Render
app = Flask("")

@app.route("/")
def home():
    return "Bot is running!"

def run():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

def keep_alive():
    t = Thread(target=run)
    t.start()

# Gmail generator
def generate_gmails(gmail, count):
    username, domain = gmail.split("@")
    variations = []
    letters = [c for c in username]
    for p in product(*[[c.lower(), c.upper()] if c.isalpha() else [c] for c in letters]):
        variations.append("".join(p) + "@" + domain)
        if len(variations) >= count:
            break
    return variations

# Handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send me a Gmail address:")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    if "@" not in text:
        await update.message.reply_text("Invalid Gmail. Try again.")
        return

    keyboard = [
        [InlineKeyboardButton("100", callback_data=f"{text}|100"),
         InlineKeyboardButton("200", callback_data=f"{text}|200")],
        [InlineKeyboardButton("500", callback_data=f"{text}|500"),
         InlineKeyboardButton("1000", callback_data=f"{text}|1000")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Select number of Gmail variations:", reply_markup=reply_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    gmail, count = query.data.split("|")
    count = int(count)
    variations = generate_gmails(gmail, count)
    msg = "\n".join(variations)
    if len(msg) > 4000:
        msg = "\n".join(variations[:50]) + "\n... (truncated)"
    await query.edit_message_text(f"Generated {len(variations)} Gmail(s):\n{msg}")

def main():
    keep_alive()  # Start dummy server

    app_bot = ApplicationBuilder().token(BOT_TOKEN).build()
    app_bot.add_handler(CommandHandler("start", start))
    app_bot.add_handler(CommandHandler("help", start))
    app_bot.add_handler(CallbackQueryHandler(button))
    app_bot.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    print("Bot started successfully!")
    app_bot.run_polling()

if __name__ == "__main__":
    main()
