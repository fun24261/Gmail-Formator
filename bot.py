from itertools import product
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = "8107648163:AAH5pbOD_yjOHdV8yWiN3Zw702bNOl7LmpQ"

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
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send me a Gmail address:")

# Handle messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    if "@" not in text:
        await update.message.reply_text("Invalid Gmail. Try again.")
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
    await update.message.reply_text("Select number of Gmail variations:", reply_markup=reply_markup)

# Handle button presses
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    gmail, count = query.data.split("|")
    count = int(count)
    variations = generate_gmails(gmail, count)
    msg = "\n".join(variations)
    if len(msg) > 4000:  # Telegram message limit
        msg = "\n".join(variations[:50]) + "\n... (truncated)"
    await query.edit_message_text(f"Generated {len(variations)} Gmail(s):\n{msg}")

# Main function
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", start))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    print("Bot started successfully!")
    app.run_polling()

if __name__ == "__main__":
    main()
