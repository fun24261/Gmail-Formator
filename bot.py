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


# 🔹 Foreign Name Database (30 names per country)
foreign_data = {
    "saudi": [
        ("أحمد", "محمد"), ("يوسف", "عبدالله"), ("علي", "سلمان"), ("خالد", "حسن"),
        ("سعيد", "فهد"), ("إبراهيم", "ماجد"), ("حسن", "ناصر"), ("سلمان", "رامي"),
        ("طارق", "ناصر"), ("عبدالرحمن", "سعيد"), ("ناصر", "عبدالله"), ("سامي", "فواز"),
        ("عمر", "حسين"), ("محمد", "أكرم"), ("فهد", "خالد"), ("عبدالله", "مازن"),
        ("رائد", "سالم"), ("هشام", "علي"), ("مازن", "سلمان"), ("رامي", "أحمد"),
        ("سيف", "ناصر"), ("بدر", "خالد"), ("أنس", "سعيد"), ("ريان", "فهد"),
        ("زيد", "سالم"), ("محمود", "طارق"), ("عماد", "سامي"), ("إيهاب", "رامي"),
        ("فارس", "مازن"), ("زيدان", "أحمد")
    ],
    "ecuador": [
        ("Carlos", "Vega"), ("Miguel", "Lopez"), ("Juan", "Torres"), ("Diego", "Mendoza"),
        ("Luis", "Gomez"), ("Andres", "Perez"), ("Jorge", "Cordero"), ("Ricardo", "Ramos"),
        ("Jose", "Castillo"), ("Pablo", "Moreno"), ("Mateo", "Ortiz"), ("Fernando", "Acosta"),
        ("Leonardo", "Gallo"), ("Cristian", "Serrano"), ("Mario", "Paredes"), ("Gabriel", "Silva"),
        ("Daniel", "Torres"), ("Eduardo", "Cruz"), ("Rafael", "Navarro"), ("Francisco", "Arias"),
        ("Rodrigo", "Bravo"), ("Hugo", "Salinas"), ("Julio", "Valdez"), ("Esteban", "Camacho"),
        ("Victor", "Rojas"), ("Oscar", "Paz"), ("Mauricio", "Soto"), ("Nicolas", "Reyes"),
        ("Javier", "Martinez"), ("Adrian", "Molina")
    ],
    "sudan": [
        ("أحمد", "محمد"), ("يوسف", "عبدالله"), ("علي", "حسن"), ("خالد", "سعيد"),
        ("سلمان", "فهد"), ("إبراهيم", "طارق"), ("حسن", "مازن"), ("سامي", "رامي"),
        ("فهد", "عبدالله"), ("عبدالرحمن", "سالم"), ("ناصر", "سعيد"), ("طارق", "خالد"),
        ("مازن", "سامي"), ("رامي", "زيد"), ("سعيد", "أنس"), ("سلمان", "ريان"),
        ("فواز", "هشام"), ("مازن", "عبدالله"), ("خالد", "سامي"), ("أحمد", "زيدان"),
        ("رامي", "فهد"), ("سامي", "حسين"), ("زيد", "سلمان"), ("أنس", "رامي"),
        ("هشام", "مازن"), ("سالم", "أحمد"), ("فهد", "طارق"), ("رامي", "خالد"), ("مازن", "سامي")
    ],
    "nicaragua": [
        ("Juan", "Ramirez"), ("Carlos", "Morales"), ("Luis", "Gomez"), ("Miguel", "Lopez"),
        ("Diego", "Torres"), ("Andres", "Perez"), ("Jorge", "Ramos"), ("Ricardo", "Castillo"),
        ("Jose", "Vega"), ("Pablo", "Soto"), ("Mateo", "Ortiz"), ("Fernando", "Navarro"),
        ("Leonardo", "Acosta"), ("Cristian", "Bravo"), ("Mario", "Silva"), ("Gabriel", "Rojas"),
        ("Daniel", "Mendoza"), ("Eduardo", "Camacho"), ("Rafael", "Paredes"), ("Francisco", "Reyes"),
        ("Rodrigo", "Arias"), ("Hugo", "Valdez"), ("Julio", "Martinez"), ("Esteban", "Gallo"),
        ("Victor", "Serrano"), ("Oscar", "Lopez"), ("Mauricio", "Vega"), ("Nicolas", "Torres"),
        ("Javier", "Ramos"), ("Adrian", "Cruz")
    ],
    "random": [
        ("Luis", "Fernandez"), ("Diego", "Santos"), ("Miguel", "Cruz"), ("Carlos", "Ramirez"),
        ("Juan", "Morales"), ("Fernando", "Lopez"), ("Rafael", "Navarro"), ("Jose", "Perez"),
        ("Mateo", "Gomez"), ("Andres", "Rojas"), ("Gabriel", "Torres"), ("Rodrigo", "Ortiz"),
        ("Eduardo", "Soto"), ("Pablo", "Silva"), ("Javier", "Valdez"), ("Esteban", "Bravo"),
        ("Victor", "Mendoza"), ("Ricardo", "Acosta"), ("Hugo", "Gallo"), ("Mario", "Castillo"),
        ("Cristian", "Serrano"), ("Diego", "Reyes"), ("Luis", "Martinez"), ("Juan", "Perez"),
        ("Miguel", "Rojas"), ("Carlos", "Ortiz"), ("Jose", "Lopez"), ("Pablo", "Gomez"),
        ("Mateo", "Ramirez"), ("Fernando", "Torres")
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

# 🔹 Dictionary to keep user context
user_context = {}  # user_id: "gmail" or "foreign"

# 🔹 /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📧 Gmail Generator", callback_data="gmail_option")],
        [InlineKeyboardButton("🌍 Foreign Name", callback_data="foreign_option")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "স্বাগতম! দুটি ফিচার ব্যবহার করতে পারেন:\n\n"
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

# 🔹 Handle Gmail input
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_context.get(user_id) == "gmail":
        gmail = update.message.text.strip()
        if "@" not in gmail:
            await update.message.reply_text("⚠️ Invalid Gmail. আবার চেষ্টা করুন।")
            return
        await update.message.reply_text("⏳ Gmail variations তৈরি হচ্ছে...")
        variations = generate_gmails(gmail)
        msg = "\n".join(variations)
        await send_long_message(update.message.chat_id, msg, context)
        await update.message.reply_text(f"✅ মোট {len(variations)}টি Gmail variation তৈরি হয়েছে!")
        user_context.pop(user_id)  # reset context
    else:
        await update.message.reply_text("⚠️ দয়া করে প্রথমে একটি ফিচার সিলেক্ট করুন।")

# 🔹 Handle callback buttons
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    user_id = query.from_user.id
    await query.answer()

    # Gmail Generator
    if data == "gmail_option":
        user_context[user_id] = "gmail"
        await query.message.reply_text("দয়া করে একটি Gmail পাঠান (উদাহরণ: example@gmail.com)")

    # Foreign Name
    elif data == "foreign_option":
        user_context[user_id] = "foreign"
        keyboard = [
            [InlineKeyboardButton("🇸🇦 Saudi Arabia", callback_data="country_saudi")],
            [InlineKeyboardButton("🇪🇨 Ecuador", callback_data="country_ecuador")],
            [InlineKeyboardButton("🇸🇩 Sudan", callback_data="country_sudan")],
            [InlineKeyboardButton("🇳🇮 Nicaragua", callback_data="country_nicaragua")],
            [InlineKeyboardButton("🌐 Random Country", callback_data="country_random")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text("একটি দেশ নির্বাচন করুন 👇", reply_markup=reply_markup)

    # Show one random name with Change button
    elif data.startswith("country_"):
        country_key = data.split("_")[1]
        names = foreign_data.get(country_key, [])
        first, last = random.choice(names)
        username = f"@{first.lower()}_{last.lower().replace('-', '')}{random.randint(10,99)}"
        keyboard = [
            [InlineKeyboardButton("🔄 Change", callback_data=f"country_{country_key}")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text=f"{first} {last} → {username}",
            reply_markup=reply_markup
        )

# 🔹 Main function
def main():
    keep_alive()  # Flask server for Render Free Plan

    app_bot = ApplicationBuilder().token(BOT_TOKEN).build()
    app_bot.add_handler(CommandHandler("start", start))
    app_bot.add_handler(CallbackQueryHandler(button))
    app_bot.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_text))

    print("✅ Bot started successfully on Render!")
    app_bot.run_polling()

if __name__ == "__main__":
    main()
