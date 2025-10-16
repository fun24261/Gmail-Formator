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
        ("Andres", "Mora", "@andres_mora137"),
        ("Pedro", "Navarro", "@pedro_navarro138"),
        ("Luis", "Gutierrez", "@luis_gutierrez139"),
        ("Diego", "Paredes", "@diego_paredes140"),
        ("Miguel", "Ortiz", "@miguel_ortiz141"),
        ("Carlos", "Silva", "@carlos_silva142"),
        ("Jorge", "Garcia", "@jorge_garcia143"),
        ("Eduardo", "Salinas", "@eduardo_salinas144"),
        ("Fernando", "Cordero", "@fernando_cordero145"),
        ("Alberto", "Lozano", "@alberto_lozano146"),
        ("Rafael", "Vega", "@rafael_vega147"),
        ("Sergio", "Pinto", "@sergio_pinto148"),
        ("Martin", "Morales", "@martin_morales149"),
        ("Joaquin", "Vasquez", "@joaquin_vasquez150"),
        ("Ricardo", "Diaz", "@ricardo_diaz151"),
        ("Victor", "Santos", "@victor_santos152"),
        ("Oscar", "Perez", "@oscar_perez153"),
        ("Manuel", "Fuentes", "@manuel_fuentes154"),
        ("Francisco", "Reyes", "@francisco_reyes155"),
        ("Andres", "Lozano", "@andres_lozano156"),
        ("Pedro", "Romero", "@pedro_romero157"),
    ],
}

# User Context Dictionary: user_id -> {"mode": "gmail"/"foreign", "country": "saudi"/etc, "index": 0, "gmail_parts": [..]}
user_context = {}

# Generate Gmail variations function
def generate_gmail_variations(name_parts):
    """
    Generates up to MAX_VARIATIONS Gmail variations by joining name parts with dots.
    """
    parts = name_parts.copy()
    # Generate all possible combinations with dots or no dots
    all_combinations = set()

    # We consider dot or no dot between every part (except the last)
    # Example for 3 parts: parts = [p1, p2, p3]
    # possibilities: p1p2p3, p1.p2p3, p1p2.p3, p1.p2.p3
    def backtrack(idx, current):
        if idx == len(parts):
            all_combinations.add("".join(current))
            return
        # Append without dot (except if idx == 0)
        if idx > 0:
            current.append(parts[idx])
            backtrack(idx + 1, current)
            current.pop()
            current.append("." + parts[idx])
            backtrack(idx + 1, current)
            current.pop()
        else:
            current.append(parts[idx])
            backtrack(idx + 1, current)
            current.pop()

    backtrack(0, [])
    result = list(all_combinations)[:MAX_VARIATIONS]
    return result

# Telegram Bot Handlers

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "Welcome! Choose one option:\n"
        "1. Generate Gmail Variations\n"
        "2. Foreign Names\n\n"
        "Send /gmail to start Gmail variation.\n"
        "Send /foreign to see Foreign names."
    )
    await update.message.reply_text(text)

async def gmail_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_context[user_id] = {"mode": "gmail"}
    await update.message.reply_text("Send me your full name (first, middle, last) separated by spaces:")

async def foreign_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_context[user_id] = {"mode": "foreign"}
    # Show country options as buttons
    buttons = [
        [InlineKeyboardButton("Saudi 🇸🇦", callback_data="country_saudi"),
         InlineKeyboardButton("Sudan 🇸🇩", callback_data="country_sudan")],
        [InlineKeyboardButton("Ecuador 🇪🇨", callback_data="country_ecuador"),
         InlineKeyboardButton("Random", callback_data="country_random")],
    ]
    await update.message.reply_text("Choose a country:", reply_markup=InlineKeyboardMarkup(buttons))

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    text = update.message.text.strip()
    ctx = user_context.get(user_id, {})

    if ctx.get("mode") == "gmail":
        # Split name parts
        parts = text.split()
        if len(parts) < 2:
            await update.message.reply_text("Please send at least two name parts.")
            return

        # Save parts for generating variations
        user_context[user_id]["gmail_parts"] = parts
        variations = generate_gmail_variations(parts)
        variations_text = "\n".join(variations[:20])  # Show first 20 only for brevity
        await update.message.reply_text(f"Here are some Gmail variations:\n{variations_text}\n\nSend /gmail again to try new name.")
    
    else:
        await update.message.reply_text("Please choose /gmail or /foreign first.")

async def callback_query_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    data = query.data
    ctx = user_context.get(user_id, {})

    # Handle country selection or "Change" in foreign mode
    if data.startswith("country_"):
        country = data.split("_")[1]
        names = foreign_data.get(country, [])

        if not names:
            await query.message.reply_text("No data found for this country.")
            return

        # Initialize or update index for this user and country
        if ctx.get("mode") != "foreign" or ctx.get("country") != country:
            user_context[user_id] = {"mode": "foreign", "country": country, "index": 0}
        else:
            current_index = ctx.get("index", 0)
            next_index = (current_index + 1) % len(names)
            user_context[user_id]["index"] = next_index

        index = user_context[user_id]["index"]
        first_name, last_name, tg_username = names[index]

        keyboard = [[InlineKeyboardButton("🔄 Change", callback_data=f"country_{country}")]]
        await query.edit_message_text(
            text=f"{first_name} {last_name} → {tg_username}\n\n[{index+1}/{len(names)}]",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    else:
        await query.message.reply_text("Unknown command.")

# Main function to start bot and flask server
def main():
    keep_alive()

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("gmail", gmail_command))
    app.add_handler(CommandHandler("foreign", foreign_command))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    app.add_handler(CallbackQueryHandler(callback_query_handler))

    print("Bot started...")
    app.run_polling()

if __name__ == "__main__":
    main()
