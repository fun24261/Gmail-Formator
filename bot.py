from itertools import product
from threading import Thread
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler,
    MessageHandler, ContextTypes, filters
)
import random

# 🔑 তোমার বট টোকেন
BOT_TOKEN = "8107648163:AAH5pbOD_yjOHdV8yWiN3Zw702bNOl7LmpQ"

# Gmail generator limit
MAX_VARIATIONS = 10000

# 🔹 Dummy Flask server (Render free plan compatible)
flask_app = Flask("")

@flask_app.route("/")
def home():
    return "Bot is running successfully!"

def run_flask():
    flask_app.run(host="0.0.0.0", port=5000)

def keep_alive():
    t = Thread(target=run_flask)
    t.start()


# 🔹 Foreign Name Database
foreign_data = {
    "saudi": [
        ("Omar", "Al-Farhan"), ("Faisal", "Bin-Hassan"), ("Abdullah", "Al-Mutairi"),
        ("Yusuf", "Al-Qahtani"), ("Hassan", "Al-Salem"), ("Ali", "Al-Faisal"),
        ("Khalid", "Al-Rashid"), ("Sultan", "Al-Otaibi"), ("Majed", "Al-Amri"),
        ("Tariq", "Al-Harbi"), ("Salman", "Al-Zahrani"), ("Ibrahim", "Al-Saadi"),
        ("Mansour", "Al-Ahmad"), ("Saad", "Al-Dosari"), ("Rashid", "Al-Shammari"),
        ("Hamad", "Al-Mansour"), ("Anas", "Al-Najjar"), ("Nasser", "Al-Jabri"),
        ("Turki", "Al-Mutlaq"), ("Waleed", "Al-Khalifa"), ("Badr", "Al-Shehri"),
        ("Talal", "Al-Subaie"), ("Fahad", "Al-Ruwais"), ("Othman", "Al-Ali"),
        ("Rayan", "Al-Jaber"), ("Adnan", "Al-Masri"), ("Ziad", "Al-Saif"),
        ("Sami", "Al-Bakr"), ("Ammar", "Al-Nasser"), ("Imran", "Al-Salem")
    ],
    "ecuador": [
        ("Carlos", "Vega"), ("Miguel", "Lopez"), ("Juan", "Torres"),
        ("Diego", "Mendoza"), ("Luis", "Gomez"), ("Andres", "Perez"),
        ("Jorge", "Cordero"), ("Ricardo", "Ramos"), ("Jose", "Castillo"),
        ("Pablo", "Moreno"), ("Mateo", "Ortiz"), ("Fernando", "Acosta"),
        ("Leonardo", "Gallo"), ("Cristian", "Serrano"), ("Mario", "Paredes"),
        ("Gabriel", "Silva"), ("Daniel", "Torres"), ("Eduardo", "Cruz"),
        ("Rafael", "Navarro"), ("Francisco", "Arias"), ("Rodrigo", "Bravo"),
        ("Hugo", "Salinas"), ("Julio", "Valdez"), ("Esteban", "Camacho"),
        ("Victor", "Rojas"), ("Oscar", "Paz"), ("Mauricio", "Soto"),
        ("Nicolas", "Reyes"), ("Javier", "Martinez"), ("Adrian", "Molina")
    ]
}


# 🔹 Gmail variation generator
def generate_gmails(gmail):
    username, domain = gmail.split("@")
    variations = []
    letters = [c for c in username]
    for p in product(*[[c.lower(), c.upper()] if c.isalpha() else [c] for c in letters]):
        variations.append("".join(p) + "@" + domain)
        if len(variations) >= MAX_VARIATIONS:
            break
    return variations


# 🔹 /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📧 Gmail Generator", callback_data="gmail_option")],
        [InlineKeyboardButton("🌍 Foreign Name", callback_data="foreign_option")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "স্বাগতম! আপনি দুটি ফিচার ব্যবহার করতে পারেন:\n\n"
        "1️⃣ Gmail Generator\n"
        "2️⃣ Foreign Name\n\n"
        "নিচের বাটন থেকে একটি অপশন বাছাই করুন 👇",
        reply_markup=reply_markup
    )


# 🔹 Send long messages safely
async def send_long_message(chat_id, text, context):
    chunk_size = 4000
    for i in range(0, len(text), chunk_size):
        await context.bot.send_message(chat_id, text[i:i+chunk_size])


# 🔹 Handle Gmail
async def handle_gmail(update: Update, context: ContextTypes.DEFAULT_TYPE):
    gmail = update.message.text.strip()
    if "@" not in gmail:
        await update.message.reply_text("⚠️ Invalid Gmail. আবার চেষ্টা করুন।")
        return

    await update.message.reply_text("⏳ Gmail variations তৈরি হচ্ছে...")

    variations = generate_gmails(gmail)
    msg = "\n".join(variations)
    await send_long_message(update.message.chat_id, msg, context)
    await update.message.reply_text(f"✅ মোট {len(variations)}টি Gmail variation তৈরি হয়েছে!")


# 🔹 Handle callback buttons
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    await query.answer()

    if data == "gmail_option":
        await query.message.reply_text("দয়া করে একটি Gmail পাঠান (উদাহরণ: example@gmail.com)")

    elif data == "foreign_option":
        keyboard = [
            [InlineKeyboardButton("🇸🇦 সৌদি আরব", callback_data="country_saudi")],
            [InlineKeyboardButton("🇪🇨 ইকুয়েডর", callback_data="country_ecuador")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text("একটি দেশ নির্বাচন করুন 👇", reply_markup=reply_markup)

    elif data.startswith("country_"):
        country_key = data.split("_")[1]
        names = foreign_data.get(country_key, [])
        result_text = f"🌍 {country_key.capitalize()} দেশের নামের তালিকা:\n\n"
        for first, last in names:
            username = f"@{first.lower()}_{last.lower().replace('-', '')}{random.randint(10,99)}"
            result_text += f"{first} {last} → {username}\n"
        await send_long_message(query.message.chat_id, result_text, context)
        await query.edit_message_text(f"{country_key.capitalize()} দেশের নাম পাঠানো হয়েছে ✅")


# 🔹 Main function
def main():
    keep_alive()  # Flask server for Render Free Plan

    app_bot = ApplicationBuilder().token(BOT_TOKEN).build()
    app_bot.add_handler(CommandHandler("start", start))
    app_bot.add_handler(CallbackQueryHandler(button))
    app_bot.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_gmail))

    print("✅ Bot started successfully on Render!")
    app_bot.run_polling()


if __name__ == "__main__":
    main()
