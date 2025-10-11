from itertools import product
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, CallbackContext

# সরাসরি Bot Token
BOT_TOKEN = "8107648163:AAH5pbOD_yjOHdV8yWiN3Zw702bNOl7LmpQ"

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is missing!")

# Gmail variation generator
def generate_gmails(gmail, count):
    username, domain = gmail.split("@")
    variations = []

    letters = [c for c in username]
    for p in product(*[[c.lower(), c.upper()] if c.isalpha() else [c] for c in letters]):
        variations.append("".join(p) + "@" + domain)
        if len(variations) >= count:
            break
    return variations

# /start command
def start(update: Update, context: CallbackContext):
    update.message.reply_text("Send me a Gmail address:")

# Handle messages
def handle_message(update: Update, context: CallbackContext):
    text = update.message.text.strip()
    if "@" not in text:
        update.message.reply_text("Invalid Gmail. Try again.")
        return

    keyboard = [
        [
            InlineKeyboardButton("100", callback_data=f"{text}|100"),
            InlineKeyboardButton("200", callback_data=f"{text}|200"),
        ],
        [
            InlineKeyboardButton("500", callback_data=f"{text}|500"),
            InlineKeyboardButton("1000", callback_data=f"{text}|1000"),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Select number of Gmail variations:", reply_markup=reply_markup)

# Handle button presses
def button(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    gmail, count = query.data.split("|")
    count = int(count)
    variations = generate_gmails(gmail, count)
    msg = "\n".join(variations)
    if len(msg) > 4000:  # Telegram message limit
        msg = "\n".join(variations[:50]) + "\n... (truncated)"
    query.edit_message_text(f"Generated {len(variations)} Gmail(s):\n{msg}")

# Main function
def main():
    updater = Updater(token=BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", start))
    dp.add_handler(CallbackQueryHandler(button))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    print("Bot started successfully!")
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
