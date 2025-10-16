from itertools import product
from threading import Thread
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler,
    MessageHandler, ContextTypes, filters
)

# ✅ Telegram Bot Token
BOT_TOKEN = "8107648163:AAH5pbOD_yjOHdV8yWiN3Zw702bNOl7LmpQ"

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

# ✅ Foreign Names with Telegram usernames (30 each)
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
        ("فهد", "أحمد", "@fahad_ahmad30")
    ],
    "ecuador": [
        ("Carlos", "Vega", "@carlos_vega01"),
        ("Miguel", "Lopez", "@miguel_lopez02"),
        ("Juan", "Torres", "@juan_torres03"),
        ("Diego", "Mendoza", "@diego_mendoza04"),
        ("Luis", "Fernandez", "@luis_fernandez05"),
        ("Pedro", "Martinez", "@pedro_martinez06"),
        ("Jorge", "Rojas", "@jorge_rojas07"),
        ("Andres", "Gomez", "@andres_gomez08"),
        ("Ricardo", "Castro", "@ricardo_castro09"),
        ("Francisco", "Salazar", "@francisco_salazar10"),
        ("Manuel", "Perez", "@manuel_perez11"),
        ("Rafael", "Diaz", "@rafael_diaz12"),
        ("Hector", "Cruz", "@hector_cruz13"),
        ("Oscar", "Alvarez", "@oscar_alvarez14"),
        ("Victor", "Santos", "@victor_santos15"),
        ("Eduardo", "Ramos", "@eduardo_ramos16"),
        ("Javier", "Ortega", "@javier_ortega17"),
        ("Felipe", "Gutierrez", "@felipe_gutierrez18"),
        ("Diego", "Paredes", "@diego_paredes19"),
        ("Marco", "Vargas", "@marco_vargas20"),
        ("Alberto", "Romero", "@alberto_romero21"),
        ("Gustavo", "Navarro", "@gustavo_navarro22"),
        ("Sergio", "Mora", "@sergio_mora23"),
        ("Martin", "Fuentes", "@martin_fuentes24"),
        ("Joaquin", "Reyes", "@joaquin_reyes25"),
        ("Carlos", "Ortiz", "@carlos_ortiz26"),
        ("Fernando", "Silva", "@fernando_silva27"),
        ("Luis", "Garcia", "@luis_garcia28"),
        ("Andres", "Salinas", "@andres_salinas29"),
        ("Pedro", "Cordero", "@pedro_cordero30")
    ],
    "random": [
        ("Luis", "Fernandez", "@luis_fernandez31"),
        ("Diego", "Santos", "@diego_santos32"),
        ("Miguel", "Cruz", "@miguel_cruz33"),
        ("Carlos", "Ramirez", "@carlos_ramirez34"),
        ("Jorge", "Lopez", "@jorge_lopez35"),
        ("Eduardo", "Mendoza", "@eduardo_mendoza36"),
        ("Fernando", "Garcia", "@fernando_garcia37"),
        ("Alberto", "Vargas", "@alberto_vargas38"),
        ("Rafael", "Ortega", "@rafael_ortega39"),
        ("Sergio", "Diaz", "@sergio_diaz40"),
        ("Martin", "Castro", "@martin_castro41"),
        ("Joaquin", "Salazar", "@joaquin_salazar42"),
        ("Ricardo", "Perez", "@ricardo_perez43"),
        ("Victor", "Fuentes", "@victor_fuentes44"),
        ("Oscar", "Reyes", "@oscar_reyes45"),
        ("Manuel", "Lozano", "@manuel_lozano46"),
        ("Francisco", "Romero", "@francisco_romero47"),
        ("Andres", "Mora", "@andres_mora48"),
        ("Pedro", "Navarro", "@pedro_navarro49"),
        ("Luis", "Gutierrez", "@luis_gutierrez50"),
        ("Diego", "Paredes", "@diego_paredes51"),
        ("Miguel", "Ortiz", "@miguel_ortiz52"),
        ("Carlos", "Silva", "@carlos_silva53"),
        ("Jorge", "Garcia", "@jorge_garcia54"),
        ("Eduardo", "Salinas", "@eduardo_salinas55"),
        ("Fernando", "Cordero", "@fernando_cordero56"),
        ("Alberto", "Lozano", "@alberto_lozano57"),
        ("Rafael", "Vega", "@rafael_vega58"),
        ("Sergio", "Pinto", "@sergio_pinto59"),
        ("Martin", "Morales", "@martin_morales60")
    ]
}

# Global storage for user data
user_gmail_data = {}
user_foreign_data = {}

# Generate case variations for Gmail username
def generate_case_variations(username):
    variations = set()
    username_lower = username.lower()
    
    # Generate all possible case combinations
    for i in range(2 ** len(username_lower)):
        variation = []
        for j, char in enumerate(username_lower):
            if (i >> j) & 1:
                variation.append(char.upper())
            else:
                variation.append(char)
        variations.add(''.join(variation))
    
    return list(variations)

# Telegram Bot Handlers

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    user_name = user.first_name
    
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
    
    keyboard = [
        [InlineKeyboardButton("📧 Gmail Generator", callback_data="main_gmail")],
        [InlineKeyboardButton("🌍 Foreign Names", callback_data="main_foreign")]
    ]
    
    text = "🏠 Main Menu - Please choose a service:"
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

async def main_gmail_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    
    # Check if user has existing Gmail data
    if user_id in user_gmail_data and user_gmail_data[user_id]["variations"]:
        variations = user_gmail_data[user_id]["variations"]
        current_index = user_gmail_data[user_id]["current_index"]
        total_count = len(variations)
        remaining = total_count - current_index
        
        if remaining > 0:
            keyboard = [
                [InlineKeyboardButton(f"📧 Send Gmail ({remaining} left)", callback_data="send_gmail")],
                [InlineKeyboardButton("🔄 New Gmail", callback_data="new_gmail")],
                [InlineKeyboardButton("🔙 Main Menu", callback_data="main_menu")]
            ]
            
            text = (
                f"📧 **Gmail Generator**\n\n"
                f"You have **{remaining}** variations remaining from previous session.\n\n"
                f"Click 'Send Gmail' to continue receiving variations.\n"
                f"Or click 'New Gmail' to generate new variations."
            )
            await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')
            return
    
    # If no existing data, show normal Gmail input
    text = (
        "📧 **Gmail Generator**\n\n"
        "Please send me your complete Gmail address.\n\n"
        "Example: `john.doe@gmail.com`\n\n"
        "I will generate all possible case variations for the username part!"
    )
    
    keyboard = [[InlineKeyboardButton("🔙 Main Menu", callback_data="main_menu")]]
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

async def new_gmail_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    text = (
        "📧 **New Gmail Variations**\n\n"
        "Please send me your complete Gmail address.\n\n"
        "Example: `john.doe@gmail.com`\n\n"
        "I will generate all possible case variations for the username part!"
    )
    
    keyboard = [[InlineKeyboardButton("🔙 Main Menu", callback_data="main_menu")]]
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

async def main_foreign_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    # Show country options as buttons
    buttons = [
        [InlineKeyboardButton("🇸🇦 Saudi Arabia", callback_data="country_saudi")],
        [InlineKeyboardButton("🇪🇨 Ecuador", callback_data="country_ecuador")],
        [InlineKeyboardButton("🌍 Random Names", callback_data="country_random")],
        [InlineKeyboardButton("🔙 Main Menu", callback_data="main_menu")]
    ]
    
    text = "🌍 **Foreign Names**\n\nPlease choose a country:"
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(buttons), parse_mode='Markdown')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    text = update.message.text.strip()

    # Check if it's a Gmail address for variation generation
    if text and not text.startswith('/') and '@gmail.com' in text:
        # Extract username from Gmail address
        username = text.split('@')[0].strip()
        
        if not username:
            await update.message.reply_text("Please send a valid Gmail address.")
            return
        
        # Generate case variations
        variations = generate_case_variations(username)
        
        # Store in global storage
        user_gmail_data[user_id] = {
            "variations": variations,
            "current_index": 0
        }
        
        total_count = len(variations)
        
        # Create keyboard with remaining count
        keyboard = [
            [InlineKeyboardButton(f"📧 Send Gmail ({total_count} left)", callback_data="send_gmail")],
            [InlineKeyboardButton("🔙 Main Menu", callback_data="main_menu")]
        ]
        
        await update.message.reply_text(
            f"✅ **Successfully generated {total_count} case variations!**\n\n"
            f"Click the button below to receive variations one by one:",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown'
        )
    
    elif text and not text.startswith('/'):
        await update.message.reply_text("Please send a valid Gmail address (e.g., example@gmail.com)")
    
    else:
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
        
    # Handle New Gmail Option
    elif data == "new_gmail":
        await new_gmail_handler(update, context)
        return

    # Handle Main Foreign Option
    elif data == "main_foreign":
        await main_foreign_handler(update, context)
        return

    # Handle Gmail sending
    elif data == "send_gmail":
        if user_id not in user_gmail_data or not user_gmail_data[user_id]["variations"]:
            await query.message.reply_text("No Gmail variations found. Please send your Gmail address first.")
            return
        
        variations = user_gmail_data[user_id]["variations"]
        current_index = user_gmail_data[user_id]["current_index"]
        
        if current_index < len(variations):
            # Send current variation (one at a time)
            variation = variations[current_index]
            await context.bot.send_message(
                chat_id=query.message.chat_id,
                text=f"{variation}@gmail.com"
            )
            
            # Update index
            user_gmail_data[user_id]["current_index"] += 1
            
            # Update button with remaining count
            remaining = len(variations) - user_gmail_data[user_id]["current_index"]
            
            if remaining > 0:
                keyboard = [
                    [InlineKeyboardButton(f"📧 Send Gmail ({remaining} left)", callback_data="send_gmail")],
                    [InlineKeyboardButton("🔙 Main Menu", callback_data="main_menu")]
                ]
                
                try:
                    await query.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup(keyboard))
                except:
                    # If message can't be edited, send new one
                    pass
            else:
                # All variations sent
                await query.message.edit_reply_markup(reply_markup=None)
                await context.bot.send_message(
                    chat_id=query.message.chat_id,
                    text="✅ **All Gmail variations have been sent!**\n\nUse the buttons below to generate new variations:",
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("📧 New Gmail", callback_data="new_gmail")],
                        [InlineKeyboardButton("🏠 Main Menu", callback_data="main_menu")]
                    ]),
                    parse_mode='Markdown'
                )
    
    # Handle country selection for foreign names
    elif data.startswith("country_"):
        country = data.split("_")[1]
        names = foreign_data.get(country, [])

        if not names:
            await query.message.reply_text("No data found for this country.")
            return

        if user_id not in user_foreign_data:
            user_foreign_data[user_id] = {"country": country, "current_index": 0}
        else:
            user_foreign_data[user_id]["country"] = country
            user_foreign_data[user_id]["current_index"] = 0

        current_index = user_foreign_data[user_id]["current_index"]
        first_name, last_name, tg_username = names[current_index]

        country_names = {
            "saudi": "🇸🇦 Saudi Arabia",
            "ecuador": "🇪🇨 Ecuador", 
            "random": "🌍 Random Names"
        }

        keyboard = [
            [InlineKeyboardButton("🔄 Next Name", callback_data="change_foreign")],
            [InlineKeyboardButton("🔙 Back", callback_data="main_foreign"),
             InlineKeyboardButton("🏠 Main Menu", callback_data="main_menu")]
        ]
        
        await query.edit_message_text(
            text=f"**{country_names[country]}**\n\n"
                 f"👤 **Name:** {first_name} {last_name}\n"
                 f"📱 **Telegram:** {tg_username}\n\n"
                 f"📊 **{current_index+1}/{len(names)}**",
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
        
        current_index = user_foreign_data[user_id]["current_index"]
        next_index = (current_index + 1) % len(names)
        user_foreign_data[user_id]["current_index"] = next_index
        
        first_name, last_name, tg_username = names[next_index]
        
        country_names = {
            "saudi": "🇸🇦 Saudi Arabia",
            "ecuador": "🇪🇨 Ecuador",
            "random": "🌍 Random Names"
        }
        
        keyboard = [
            [InlineKeyboardButton("🔄 Next Name", callback_data="change_foreign")],
            [InlineKeyboardButton("🔙 Back", callback_data="main_foreign"),
             InlineKeyboardButton("🏠 Main Menu", callback_data="main_menu")]
        ]
        
        await query.edit_message_text(
            text=f"**{country_names[country]}**\n\n"
                 f"👤 **Name:** {first_name} {last_name}\n"
                 f"📱 **Telegram:** {tg_username}\n\n"
                 f"📊 **{next_index+1}/{len(names)}**",
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

    print("Bot started with complete features...")
    app.run_polling()

if __name__ == "__main__":
    main()
