from itertools import product
from threading import Thread
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler,
    MessageHandler, ContextTypes, filters
)
import random

# ✅ Telegram Bot Token
BOT_TOKEN = "8107648163:AAH5pbOD_yjOHdV8yWiN3Zw702bNOl7LmpQ"

# ✅ Max Gmail Variations
MAX_VARIATIONS = 10000

# ✅ Flask app for Render
flask_app = Flask(__name__)

@flask_app.route("/")
def home():
    return "Bot is running!"

def run_flask():
    flask_app.run(host="0.0.0.0", port=5000)

def keep_alive():
    t = Thread(target=run_flask)
    t.daemon = True
    t.start()


# ✅ Foreign Names with Telegram usernames (40 people each country)
foreign_data = {
    "saudi": [
        ("أحمد", "محمد", "@ahmad_mohamed01"),
        ("يوسف", "عبدالله", "@yousef_abdullah02"),
        ("علي", "سلمان", "@ali_salman03"),
        ("خالد", "حسن", "@khaled_hassan04"),
        ("سعيد", "فهد", "@saeed_fahad05"),
        ("إبراهيم", "ماجد", "@ibrahim_majed06"),
        ("حسن", "ناصر", "@hasan_nasser07"),
        ("سلمان", "رامي", "@salman_rami08"),
        ("فهد", "خالد", "@fahad_khaled09"),
        ("ناصر", "سعيد", "@nasser_saeed10"),
        ("ماجد", "إبراهيم", "@majed_ibrahim11"),
        ("رامي", "حسن", "@rami_hasan12"),
        ("محمد", "علي", "@mohamed_ali13"),
        ("عبدالله", "يوسف", "@abdullah_yousef14"),
        ("حسين", "سلمان", "@hossein_salman15"),
        ("طارق", "خالد", "@tariq_khaled16"),
        ("يوسف", "فهد", "@yousef_fahad17"),
        ("سلمان", "إبراهيم", "@salman_ibrahim18"),
        ("خالد", "ناصر", "@khaled_nasser19"),
        ("سعيد", "ماجد", "@saeed_majed20"),
        ("علي", "رامي", "@ali_rami21"),
        ("أحمد", "حسن", "@ahmad_hassan22"),
        ("محمد", "سلمان", "@mohamed_salman23"),
        ("عبدالله", "خالد", "@abdullah_khaled24"),
        ("ناصر", "يوسف", "@nasser_yousef25"),
        ("حسن", "فهد", "@hasan_fahad26"),
        ("رامي", "إبراهيم", "@rami_ibrahim27"),
        ("ماجد", "سعيد", "@majed_saeed28"),
        ("خالد", "علي", "@khaled_ali29"),
        ("فهد", "أحمد", "@fahad_ahmad30"),
        ("إبراهيم", "محمد", "@ibrahim_mohamed31"),
        ("سلمان", "عبدالله", "@salman_abdullah32"),
        ("حسن", "يوسف", "@hasan_yousef33"),
        ("سعيد", "علي", "@saeed_ali34"),
        ("طارق", "خالد", "@tariq_khaled35"),
        ("يوسف", "سلمان", "@yousef_salman36"),
        ("محمد", "حسن", "@mohamed_hasan37"),
        ("علي", "رامي", "@ali_rami38"),
        ("خالد", "ماجد", "@khaled_majed39"),
        ("فهد", "إبراهيم", "@fahad_ibrahim40"),
    ],
    "sudan": [
        ("أحمد", "محمد", "@ahmad_mohamed41"),
        ("يوسف", "عبدالله", "@yousef_abdullah42"),
        ("علي", "حسن", "@ali_hassan43"),
        ("خالد", "سعيد", "@khaled_saeed44"),
        ("سلمان", "فهد", "@salman_fahad45"),
        ("إبراهيم", "طارق", "@ibrahim_tariq46"),
        ("حسن", "مازن", "@hasan_mazen47"),
        ("سامي", "رامي", "@sami_rami48"),
        ("فهد", "أحمد", "@fahad_ahmad49"),
        ("سعيد", "خالد", "@saeed_khaled50"),
        ("طارق", "حسن", "@tariq_hasan51"),
        ("مازن", "يوسف", "@mazen_yousef52"),
        ("رامي", "سلمان", "@rami_salman53"),
        ("أحمد", "سامي", "@ahmad_sami54"),
        ("محمد", "طارق", "@mohamed_tariq55"),
        ("يوسف", "مازن", "@yousef_mazen56"),
        ("خالد", "رامي", "@khaled_rami57"),
        ("سلمان", "سعيد", "@salman_saeed58"),
        ("فهد", "إبراهيم", "@fahad_ibrahim59"),
        ("حسن", "سامي", "@hasan_sami60"),
        ("رامي", "مازن", "@rami_mazen61"),
        ("طارق", "سلمان", "@tariq_salman62"),
        ("مازن", "خالد", "@mazen_khaled63"),
        ("سامي", "فهد", "@sami_fahad64"),
        ("أحمد", "حسن", "@ahmad_hasan65"),
        ("محمد", "رامي", "@mohamed_rami66"),
        ("يوسف", "سامي", "@yousef_sami67"),
        ("خالد", "مازن", "@khaled_mazen68"),
        ("سلمان", "طارق", "@salman_tariq69"),
        ("فهد", "رامي", "@fahad_rami70"),
        ("حسن", "سامي", "@hasan_sami71"),
        ("رامي", "يوسف", "@rami_yousef72"),
        ("مازن", "خالد", "@mazen_khaled73"),
        ("سامي", "سعيد", "@sami_saeed74"),
        ("أحمد", "فهد", "@ahmad_fahad75"),
        ("محمد", "سلمان", "@mohamed_salman76"),
        ("يوسف", "خالد", "@yousef_khaled77"),
        ("خالد", "طارق", "@khaled_tariq78"),
        ("سلمان", "رامي", "@salman_rami79"),
        ("فهد", "مازن", "@fahad_mazen80"),
    ],
    "ecuador": [
        ("Carlos", "Vega", "@carlos_vega81"),
        ("Miguel", "Lopez", "@miguel_lopez82"),
        ("Juan", "Torres", "@juan_torres83"),
        ("Diego", "Mendoza", "@diego_mendoza84"),
        ("Luis", "Fernandez", "@luis_fernandez85"),
        ("Pedro", "Martinez", "@pedro_martinez86"),
        ("Jorge", "Rojas", "@jorge_rojas87"),
        ("Andres", "Gomez", "@andres_gomez88"),
        ("Ricardo", "Castro", "@ricardo_castro89"),
        ("Francisco", "Salazar", "@francisco_salazar90"),
        ("Manuel", "Perez", "@manuel_perez91"),
        ("Rafael", "Diaz", "@rafael_diaz92"),
        ("Hector", "Cruz", "@hector_cruz93"),
        ("Oscar", "Alvarez", "@oscar_alvarez94"),
        ("Victor", "Santos", "@victor_santos95"),
        ("Eduardo", "Ramos", "@eduardo_ramos96"),
        ("Javier", "Ortega", "@javier_ortega97"),
        ("Felipe", "Gutierrez", "@felipe_gutierrez98"),
        ("Diego", "Paredes", "@diego_paredes99"),
        ("Marco", "Vargas", "@marco_vargas100"),
        ("Alberto", "Romero", "@alberto_romero101"),
        ("Gustavo", "Navarro", "@gustavo_navarro102"),
        ("Sergio", "Mora", "@sergio_mora103"),
        ("Martin", "Fuentes", "@martin_fuentes104"),
        ("Joaquin", "Reyes", "@joaquin_reyes105"),
        ("Carlos", "Ortiz", "@carlos_ortiz106"),
        ("Fernando", "Silva", "@fernando_silva107"),
        ("Luis", "Garcia", "@luis_garcia108"),
        ("Andres", "Salinas", "@andres_salinas109"),
        ("Pedro", "Cordero", "@pedro_cordero110"),
        ("Jorge", "Lozano", "@jorge_lozano111"),
        ("Manuel", "Vega", "@manuel_vega112"),
        ("Rafael", "Pinto", "@rafael_pinto113"),
        ("Hector", "Morales", "@hector_morales114"),
        ("Oscar", "Vasquez", "@oscar_vasquez115"),
        ("Victor", "Diaz", "@victor_diaz116"),
        ("Eduardo", "Santos", "@eduardo_santos117"),
        ("Javier", "Perez", "@javier_perez118"),
        ("Felipe", "Martinez", "@felipe_martinez119"),
    ],
    "random": [
        ("Luis", "Fernandez", "@luis_fernandez120"),
        ("Diego", "Santos", "@diego_santos121"),
        ("Miguel", "Cruz", "@miguel_cruz122"),
        ("Carlos", "Ramirez", "@carlos_ramirez123"),
        ("Jorge", "Lopez", "@jorge_lopez124"),
        ("Eduardo", "Mendoza", "@eduardo_mendoza125"),
        ("Fernando", "Garcia", "@fernando_garcia126"),
        ("Alberto", "Vargas", "@alberto_vargas127"),
        ("Rafael", "Ortega", "@rafael_ortega128"),
        ("Sergio", "Diaz", "@sergio_diaz129"),
        ("Martin", "Castro", "@martin_castro130"),
        ("Joaquin", "Salazar", "@joaquin_salazar131"),
        ("Ricardo", "Perez", "@ricardo_perez132"),
        ("Victor", "Fuentes", "@victor_fuentes133"),
        ("Oscar", "Reyes", "@oscar_reyes134"),
        ("Manuel", "Lozano", "@manuel_lozano135"),
        ("Francisco", "Romero", "@francisco_romero136"),
        ("Andres", "Navarro", "@andres_navarro137"),
        ("Pedro", "Mora", "@pedro_mora138"),
        ("Javier", "Vasquez", "@javier_vasquez139"),
        ("Luis", "Morales", "@luis_morales140"),
        ("Diego", "Pinto", "@diego_pinto141"),
        ("Miguel", "Salinas", "@miguel_salinas142"),
        ("Carlos", "Cordero", "@carlos_cordero143"),
        ("Jorge", "Fuentes", "@jorge_fuentes144"),
        ("Eduardo", "Lopez", "@eduardo_lopez145"),
        ("Fernando", "Mendoza", "@fernando_mendoza146"),
        ("Alberto", "Garcia", "@alberto_garcia147"),
        ("Rafael", "Vargas", "@rafael_vargas148"),
        ("Sergio", "Ortega", "@sergio_ortega149"),
        ("Martin", "Diaz", "@martin_diaz150"),
        ("Joaquin", "Castro", "@joaquin_castro151"),
        ("Ricardo", "Salazar", "@ricardo_salazar152"),
        ("Victor", "Perez", "@victor_perez153"),
        ("Oscar", "Fuentes", "@oscar_fuentes154"),
        ("Manuel", "Reyes", "@manuel_reyes155"),
        ("Francisco", "Lozano", "@francisco_lozano156"),
        ("Andres", "Romero", "@andres_romero157"),
        ("Pedro", "Navarro", "@pedro_navarro158"),
    ]
}


# ✅ Gmail variation generator
def generate_gmails(gmail: str):
    username, domain = gmail.split("@", 1)
    variations = []
    pattern = [[c.lower(), c.upper()] if c.isalpha() else [c] for c in username]
    for p in product(*pattern):
        variations.append("".join(p) + "@" + domain)
        if len(variations) >= MAX_VARIATIONS:
            break
    return variations


# ✅ In-memory user context
user_context = {}  # user_id: {"mode": "gmail"/"foreign", "variations": [...], "index": int}


# ✅ /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_name = update.message.from_user.first_name

    keyboard = [
        [InlineKeyboardButton("📧 Gmail Generator", callback_data="gmail_option")],
        [InlineKeyboardButton("🌍 Foreign Name", callback_data="foreign_option")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    welcome = (
        f"স্বাগতম {user_name}! 👋\n\n"
        "দুটি ফিচার ব্যবহার করতে পারেন:\n"
        "1️⃣ Gmail Generator\n"
        "2️⃣ Foreign Name\n\n"
        "নিচের বাটন থেকে একটি অপশন বাছাই করুন:"
    )

    # Info message if old gmail exists
    if user_id in user_context and user_context[user_id].get("variations"):
        welcome += "\n\n⚠️ আপনি আগে Gmail variation তৈরি করেছিলেন। Send Gmail চাপলে সেগুলো আবার দেখতে পাবেন। নতুন Gmail দিলে আগেরটা মুছে যাবে।"

    await update.message.reply_text(welcome, reply_markup=reply_markup)


# ✅ Gmail input handler
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_data = user_context.get(user_id, {})

    if user_data.get("mode") == "gmail":
        gmail = update.message.text.strip()
        if "@" not in gmail:
            await update.message.reply_text("⚠️ সঠিক Gmail দিন (উদাহরণ: example@gmail.com)")
            return

        await update.message.reply_text("⏳ Gmail variations তৈরি হচ্ছে...")

        variations = generate_gmails(gmail)
        user_context[user_id]["variations"] = variations
        user_context[user_id]["index"] = 0

        keyboard = [[InlineKeyboardButton("📤 Send Gmail", callback_data="send_next")]]
        await update.message.reply_text(
            f"✅ {len(variations)} টি Gmail variation তৈরি হয়েছে!\n"
            "Send Gmail বাটনে চাপ দিন পেতে থাকুন 👇",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    else:
        await update.message.reply_text("⚠️ আগে Gmail Generator অপশন বাছাই করুন।")


# ✅ Callback button handler
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    user_id = query.from_user.id
    await query.answer()

    if data == "gmail_option":
        if user_id not in user_context:
            user_context[user_id] = {}
        user_context[user_id]["mode"] = "gmail"
        await query.message.reply_text("✉️ একটি Gmail পাঠান (যেমন: test@gmail.com)")

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
                keyboard = [[InlineKeyboardButton(f"📤 আরও ({remaining} বাকি)", callback_data="send_next")]]
            await query.message.reply_text(gmail, reply_markup=InlineKeyboardMarkup(keyboard) if keyboard else None)
        else:
            await query.message.reply_text("✅ সব Gmail variation পাঠানো হয়েছে!")

    elif data == "foreign_option":
        user_context[user_id] = {"mode": "foreign"}
        keyboard = [
            [InlineKeyboardButton("🇸🇦 Saudi Arabia", callback_data="country_saudi")],
            [InlineKeyboardButton("🇪🇨 Ecuador", callback_data="country_ecuador")],
            [InlineKeyboardButton("🇸🇩 Sudan", callback_data="country_sudan")],
            [InlineKeyboardButton("🌐 Random Country", callback_data="country_random")]
        ]
        await query.message.reply_text("একটি দেশ নির্বাচন করুন 👇", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data.startswith("country_"):
        country = data.split("_")[1]
        names = foreign_data.get(country, [])
        if not names:
            await query.message.reply_text("এই দেশের ডেটা নেই।")
            return

        first_name, last_name, tg_username = random.choice(names)

        keyboard = [[InlineKeyboardButton("🔄 Change", callback_data=f"country_{country}")]]
        await query.edit_message_text(
            text=f"{first_name} {last_name} → {tg_username}",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )


# ✅ Main function
def main():
    keep_alive()
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.add_handler(CallbackQueryHandler(button))

    print("Bot started...")
    app.run_polling()


if __name__ == "__main__":
    main()
