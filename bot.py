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

MAX_VARIATIONS = 10000  # Gmail generator limit

# 🔹 Flask server (Render compatible)
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
        ("أحمد", "محمد"), ("يوسف", "عبدالله"), ("علي", "سلمان"), ("خالد", "حسن"),
        ("سعيد", "فهد"), ("إبراهيم", "ماجد"), ("حسن", "ناصر"), ("سلمان", "رامي"),
        ("طارق", "ناصر"), ("عبدالرحمن", "سعيد"), ("ناصر", "عبدالله"), ("سامي", "فواز"),
        ("عمر", "حسين"), ("محمد", "أكرم"), ("فهد", "خالد"), ("عبدالله", "مازن"),
        ("رائد", "سالم"), ("هشام", "علي"), ("مازن", "সلمان"), ("رامي", "أحمد"),
        ("سيف", "ناصر"), ("بدر", "خالد"), ("أنس", "سعيد"), ("ريان", "فهد"),
        ("زيد", "سالم"), ("محمود", "طارق"), ("عماد", "سامي"), ("إيهاب", "رامি"),
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
        ("سلمان", "فهد"), ("إبراهيم", "طارق"), ("حسن", "مازن"), ("সামী", "রামী"),
        ("ফাহাদ", "আব্দুল্লাহ"), ("আব্দুর রহমান", "সালেম")
    ],
    "random": [
        ("Luis", "Fernandez"), ("Diego", "Santos"), ("Miguel", "Cruz"), ("Carlos", "Ramirez"),
        ("Juan", "Morales"), ("Fernando", "Lopez"), ("Rafael", "Navarro"), ("Jose", "Perez"),
        ("Mateo", "Gomez"), ("Andres", "Rojas"), ("Gabriel", "Torres"), ("Rodrigo", "Ortiz"),
        ("Eduardo", "Soto"), ("Pablo", "Silva"), ("Javier", "Valdez"), ("Esteban", "Bravo"),
        ("Victor", "Mendoza"), ("Ricardo", "Acosta"), ("Hugo", "Gallo"), ("Mario", "Castillo")
    ]
}


# 🔹 Gmail variation generator
def generate_gmails(gmail):
    username, domain = gmail.split("@")
    variations = []
    for p in product(*[[c.lower(), c.upper()] if c.isalpha() else [c] for c in username]):
        variations.append("".join(p) + "@" + domain)
        if len(variations) >= MAX_VARIATIONS:
            break
    return variations


# 🔹 User context
user_context = {}  # user_id: {"mode": "gmail"/"foreign", "variations": [...], "index": 0}


# 🔹 /start command (name mention added)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.message.from_user.first_name
    keyboard = [
        [InlineKeyboardButton("📧 Gmail Generator", callback_data="gmail_option")],
        [InlineKeyboardButton("🌍 Foreign Name", callback_data="foreign_option")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        f"স্বাগতম {user_name}! 👋\n\n"
        "দুটি ফিচার ব্যবহার করতে পারেন:\n\n"
        "1️⃣ Gmail Generator\n"
        "2️⃣ Foreign Name\n\n"
        "নিচের বাটন থেকে একটি অপশন বাছাই করুন 👇",
        reply_markup=reply_markup
    )


# 🔹 Gmail input
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_context.get(user_id, {}).get("mode") == "gmail":
        gmail = update.message.text.strip()
        if "@" not in gmail:
            await update.message.reply_text("⚠️ Invalid Gmail. আবার চেষ্টা করুন।")
            return

        await update.message.reply_text("⏳ Gmail variations তৈরি হচ্ছে...")
        variations = generate_gmails(gmail)
        user_context[user_id]["variations"] = variations
        user_context[user_id]["index"] = 0

        keyboard = [[InlineKeyboardButton("📤 Send Gmail", callback_data="send_next")]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(
            f"✅ মোট {len(variations)}টি Gmail variation তৈরি হয়েছে!\n\n"
            "প্রতিটি Gmail একে একে পেতে নিচের বাটনে চাপ দিন 👇",
            reply_markup=reply_markup
        )

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
        user_context[user_id] = {"mode": "gmail"}
        await query.message.reply_text("দয়া করে একটি Gmail পাঠান (উদাহরণ: example@gmail.com)")

    # Gmail send next
    elif data == "send_next":
        user_data = user_context.get(user_id, {})
        variations = user_data.get("variations", [])
        index = user_data.get("index", 0)

        if index < len(variations):
            gmail = variations[index]
            remaining = len(variations) - index - 1
            user_context[user_id]["index"] += 1

            keyboard = []
            if remaining > 0:
                keyboard = [[InlineKeyboardButton(f"📤 Send Gmail ({remaining} left)", callback_data="send_next")]]
            reply_markup = InlineKeyboardMarkup(keyboard) if keyboard else None

            await query.message.reply_text(gmail, reply_markup=reply_markup)
        else:
            await query.message.reply_text("✅ সব Gmail variation পাঠানো হয়েছে!")

    # Foreign Name
    elif data == "foreign_option":
        user_context[user_id] = {"mode": "foreign"}
        keyboard = [
            [InlineKeyboardButton("🇸🇦 Saudi Arabia", callback_data="country_saudi")],
            [InlineKeyboardButton("🇪🇨 Ecuador", callback_data="country_ecuador")],
            [InlineKeyboardButton("🇸🇩 Sudan", callback_data="country_sudan")],
            [InlineKeyboardButton("🌐 Random Country", callback_data="country_random")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text("একটি দেশ নির্বাচন করুন 👇", reply_markup=reply_markup)

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


# 🔹 Main
def main():
    keep_alive()
    app_bot = ApplicationBuilder().token(BOT_TOKEN).build()
    app_bot.add_handler(CommandHandler("start", start))
    app_bot.add_handler(CallbackQueryHandler(button))
    app_bot.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_text))

    print("✅ Bot started successfully on Render!")
    app_bot.run_polling()


if __name__ == "__main__":
    main()
