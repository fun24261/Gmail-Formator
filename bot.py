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
        ("رامي", "مازন", "@rami_mazen61"),
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

# Global storage for user data
user_gmail_data = {}  # user_id -> {"variations": [], "current_index": 0}
user_foreign_data = {}  # user_id -> {"country": "", "current_index": 0}

# Generate Gmail variations function
def generate_gmail_variations(name_parts):
    """
    Generates up to MAX_VARIATIONS Gmail variations by joining name parts with dots.
    """
    parts = [part.lower() for part in name_parts]  # Convert to lowercase for Gmail
    all_combinations = set()

    # Generate combinations with dots in different positions
    for i in range(len(parts) + 1):
        for combo in product(['', '.'], repeat=len(parts)-1):
            result = parts[0]
            for j in range(1, len(parts)):
                result += combo[j-1] + parts[j]
            all_combinations.add(result)
    
    # Also add combinations without any dots
    all_combinations.add(''.join(parts))
    
    # Limit the number of variations
    result = list(all_combinations)[:MAX_VARIATIONS]
    return result

# Telegram Bot Handlers

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    user_name = user.first_name
    
    # Create main menu buttons
    keyboard = [
        [InlineKeyboardButton("📧 Gmail Generator", callback_data="main_gmail")],
        [InlineKeyboardButton("🌍 Foreign Names", callback_data="main_foreign")]
    ]
    
    text = (
        f"Hello {user_name}! 👋 Welcome to the Name Generator Bot!\n\n"
        "Please choose a service from the buttons below:"
    )
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    # Create main menu buttons
    keyboard = [
        [InlineKeyboardButton("📧 Gmail Generator", callback_data="main_gmail")],
        [InlineKeyboardButton("🌍 Foreign Names", callback_data="main_foreign")]
    ]
    
    text = "🏠 Main Menu - Please choose a service:"
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

async def main_gmail_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    text = (
        "📧 **Gmail Generator**\n\n"
        "Please send me your full name (first, middle, last) separated by spaces.\n\n"
        "Example: `John Michael Smith`\n\n"
        "I will generate all possible Gmail variations for you!"
    )
    
    # Back button to main menu
    keyboard = [[InlineKeyboardButton("🔙 Back to Main Menu", callback_data="main_menu")]]
    
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

async def main_foreign_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    # Show country options as buttons
    buttons = [
        [InlineKeyboardButton("Saudi Arabia 🇸🇦", callback_data="country_saudi"),
         InlineKeyboardButton("Sudan 🇸🇩", callback_data="country_sudan")],
        [InlineKeyboardButton("Ecuador 🇪🇨", callback_data="country_ecuador"),
         InlineKeyboardButton("Random 🌍", callback_data="country_random")],
        [InlineKeyboardButton("🔙 Back to Main Menu", callback_data="main_menu")]
    ]
    
    text = "🌍 **Foreign Names**\n\nPlease choose a country:"
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(buttons), parse_mode='Markdown')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    text = update.message.text.strip()

    # Check if it's a name for Gmail generation
    if len(text.split()) >= 2 and not text.startswith('/'):
        # Split name parts
        parts = text.split()
        
        # Generate variations
        variations = generate_gmail_variations(parts)
        
        # Store in global storage
        user_gmail_data[user_id] = {
            "variations": variations,
            "current_index": 0
        }
        
        # Show first few variations and total count
        variations_text = "\n".join([f"`{v}`" for v in variations[:5]])  # Show first 5 only for brevity
        total_count = len(variations)
        
        # Create buttons - এখন শুধুমাত্র "Send Mail" বাটন থাকবে
        keyboard = [
            [InlineKeyboardButton("📧 Send Mail 💌", callback_data="send_gmail")],
            [InlineKeyboardButton("🔙 Back to Main Menu", callback_data="main_menu")]
        ]
        
        await update.message.reply_text(
            f"✅ **Successfully generated {total_count} Gmail variations!**\n\n"
            f"**Sample variations:**\n{variations_text}\n\n"
            f"... and **{total_count - 5}** more variations!\n\n"
            f"Click **'Send Mail 💌'** to receive variations one by one:",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown'
        )
    
    else:
        # If user sends random text, show main menu
        keyboard = [
            [InlineKeyboardButton("📧 Gmail Generator", callback_data="main_gmail")],
            [InlineKeyboardButton("🌍 Foreign Names", callback_data="main_foreign")]
        ]
        await update.message.reply_text(
            "Please choose a service from the buttons below:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

async def callback_query_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    data = query.data

    # Handle Main Menu
    if data == "main_menu":
        await show_main_menu(update, context)
        return

    # Handle Main Gmail Option
    elif data == "main_gmail":
        await main_gmail_handler(update, context)
        return

    # Handle Main Foreign Option
    elif data == "main_foreign":
        await main_foreign_handler(update, context)
        return

    # Handle Gmail sending - এখন একবারে একটি করে মেইল সেন্ড হবে
    elif data == "send_gmail":
        if user_id not in user_gmail_data or not user_gmail_data[user_id]["variations"]:
            await query.message.reply_text("No Gmail variations found. Please send your name again.")
            return
        
        variations = user_gmail_data[user_id]["variations"]
        current_index = user_gmail_data[user_id]["current_index"]
        
        if current_index < len(variations):
            # Send current variation (একটি করে)
            variation = variations[current_index]
            await context.bot.send_message(
                chat_id=query.message.chat_id,
                text=f"**{current_index + 1}. {variation}@gmail.com**",
                parse_mode='Markdown'
            )
            
            # Update index
            user_gmail_data[user_id]["current_index"] += 1
            
            # যদি আরও ভেরিয়েশন থাকে, তাহলে আবার "Send Mail" বাটন শো করবে
            if user_gmail_data[user_id]["current_index"] < len(variations):
                remaining = len(variations) - user_gmail_data[user_id]["current_index"]
                
                # শুধুমাত্র "Send Mail" বাটন থাকবে, কোন "Send All" নেই
                keyboard = [
                    [InlineKeyboardButton(f"📧 Send Next Mail 💌 ({remaining} left)", callback_data="send_gmail")],
                    [InlineKeyboardButton("🔙 Back to Main Menu", callback_data="main_menu")]
                ]
                
                # শুধু বাটন আপডেট করবে, নতুন মেসেজ সেন্ড করবে না
                try:
                    await query.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup(keyboard))
                except:
                    # যদি edit না হয়, নতুন মেসেজ সেন্ড করবে
                    await context.bot.send_message(
                        chat_id=query.message.chat_id,
                        text=f"**{remaining}** variations remaining. Click below to get next one:",
                        reply_markup=InlineKeyboardMarkup(keyboard),
                        parse_mode='Markdown'
                    )
            else:
                # সব ভেরিয়েশন সেন্ড হয়ে গেলে
                await query.message.edit_reply_markup(reply_markup=None)
                await context.bot.send_message(
                    chat_id=query.message.chat_id,
                    text="✅ **All Gmail variations have been sent!**\n\nUse the buttons below to generate new variations or explore other services:",
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("📧 New Gmail Variations", callback_data="main_gmail")],
                        [InlineKeyboardButton("🌍 Foreign Names", callback_data="main_foreign")]
                    ]),
                    parse_mode='Markdown'
                )
                # Reset index for next time
                user_gmail_data[user_id]["current_index"] = 0
    
    # Handle country selection for foreign names
    elif data.startswith("country_"):
        country = data.split("_")[1]
        names = foreign_data.get(country, [])

        if not names:
            await query.message.reply_text("No data found for this country.")
            return

        # Initialize or get user's foreign data
        if user_id not in user_foreign_data:
            user_foreign_data[user_id] = {"country": country, "current_index": 0}
        else:
            user_foreign_data[user_id]["country"] = country
            user_foreign_data[user_id]["current_index"] = 0

        current_index = user_foreign_data[user_id]["current_index"]
        first_name, last_name, tg_username = names[current_index]

        # Country display names
        country_names = {
            "saudi": "Saudi Arabia 🇸🇦",
            "sudan": "Sudan 🇸🇩", 
            "ecuador": "Ecuador 🇪🇨",
            "random": "Random 🌍"
        }

        keyboard = [
            [InlineKeyboardButton("🔄 Next Name", callback_data="change_foreign")],
            [InlineKeyboardButton("🔙 Back to Countries", callback_data="main_foreign"),
             InlineKeyboardButton("🏠 Main Menu", callback_data="main_menu")]
        ]
        
        await query.edit_message_text(
            text=f"**{country_names[country]}**\n\n"
                 f"👤 **Name:** {first_name} {last_name}\n"
                 f"📱 **Telegram:** {tg_username}\n\n"
                 f"📊 **Page:** {current_index+1}/{len(names)}",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown'
        )
    
    # Handle changing foreign names
    elif data == "change_foreign":
        if user_id not in user_foreign_data:
            await query.message.reply_text("Please select a country first.")
            return
        
        country = user_foreign_data[user_id]["country"]
        names = foreign_data.get(country, [])
        
        if not names:
            await query.message.reply_text("No data found for this country.")
            return
        
        # Move to next name (circular)
        current_index = user_foreign_data[user_id]["current_index"]
        next_index = (current_index + 1) % len(names)
        user_foreign_data[user_id]["current_index"] = next_index
        
        first_name, last_name, tg_username = names[next_index]
        
        # Country display names
        country_names = {
            "saudi": "Saudi Arabia 🇸🇦",
            "sudan": "Sudan 🇸🇩",
            "ecuador": "Ecuador 🇪🇨", 
            "random": "Random 🌍"
        }
        
        keyboard = [
            [InlineKeyboardButton("🔄 Next Name", callback_data="change_foreign")],
            [InlineKeyboardButton("🔙 Back to Countries", callback_data="main_foreign"),
             InlineKeyboardButton("🏠 Main Menu", callback_data="main_menu")]
        ]
        
        await query.edit_message_text(
            text=f"**{country_names[country]}**\n\n"
                 f"👤 **Name:** {first_name} {last_name}\n"
                 f"📱 **Telegram:** {tg_username}\n\n"
                 f"📊 **Page:** {next_index+1}/{len(names)}",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown'
        )

# Main function to start bot and flask server
def main():
    keep_alive()

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(callback_query_handler))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    print("Bot started with button interface...")
    app.run_polling()

if __name__ == "__main__":
    main()
