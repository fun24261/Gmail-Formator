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

# ✅ Foreign Names with Telegram usernames
foreign_data = {
    "saudi": [
        ("أحمد", "محمد", "@ahmad_mohamed01"),
        ("يوسف", "عبدالله", "@yousef_abdullah02"),
        ("علي", "سلمان", "@ali_salman03"),
        ("خالد", "حسن", "@khaled_hassan04"),
        ("سعيد", "فهد", "@saeed_fahad05"),
    ],
    "ecuador": [
        ("Carlos", "Vega", "@carlos_vega01"),
        ("Miguel", "Lopez", "@miguel_lopez02"),
        ("Juan", "Torres", "@juan_torres03"),
        ("Diego", "Mendoza", "@diego_mendoza04"),
        ("Luis", "Fernandez", "@luis_fernandez05"),
    ],
    "random": [
        ("Luis", "Fernandez", "@luis_fernandez31"),
        ("Diego", "Santos", "@diego_santos32"),
        ("Miguel", "Cruz", "@miguel_cruz33"),
        ("Carlos", "Ramirez", "@carlos_ramirez34"),
        ("Jorge", "Lopez", "@jorge_lopez35"),
    ]
}

# Global storage for user data
user_gmail_data = {}
user_foreign_data = {}

# Generate case variations for Gmail username
def generate_case_variations(username):
    variations = set()
    username_lower = username.lower()
    
    # Generate limited case combinations for speed
    for i in range(min(2 ** len(username_lower), 100)):
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
    
    text = f"Hello {user_name}! 👋 Welcome!\n\nPlease choose a service:"
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    keyboard = [
        [InlineKeyboardButton("📧 Gmail Generator", callback_data="main_gmail")],
        [InlineKeyboardButton("🌍 Foreign Names", callback_data="main_foreign")]
    ]
    
    await query.edit_message_text("🏠 Main Menu - Choose service:", reply_markup=InlineKeyboardMarkup(keyboard))

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
            
            text = f"📧 Gmail Generator\n\nYou have {remaining} variations remaining.\nClick 'Send Gmail' to continue."
            await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
            return
    
    text = "📧 Gmail Generator\n\nSend your Gmail address:\nExample: john.doe@gmail.com"
    keyboard = [[InlineKeyboardButton("🔙 Main Menu", callback_data="main_menu")]]
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

async def new_gmail_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    text = "📧 New Gmail\n\nSend your Gmail address:\nExample: john.doe@gmail.com"
    keyboard = [[InlineKeyboardButton("🔙 Main Menu", callback_data="main_menu")]]
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

async def main_foreign_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    buttons = [
        [InlineKeyboardButton("🇸🇦 Saudi Arabia", callback_data="saudi")],
        [InlineKeyboardButton("🇪🇨 Ecuador", callback_data="ecuador")],
        [InlineKeyboardButton("🌍 Random Names", callback_data="random")],
        [InlineKeyboardButton("🔙 Main Menu", callback_data="main_menu")]
    ]
    
    await query.edit_message_text("🌍 Foreign Names\nChoose country:", reply_markup=InlineKeyboardMarkup(buttons))

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    text = update.message.text.strip()

    # Check if it's a Gmail address
    if text and not text.startswith('/') and '@gmail.com' in text:
        username = text.split('@')[0].strip()
        
        if not username:
            await update.message.reply_text("Please send valid Gmail address.")
            return
        
        # Generate variations
        variations = generate_case_variations(username)
        
        # Store in global storage
        user_gmail_data[user_id] = {
            "variations": variations,
            "current_index": 0
        }
        
        total_count = len(variations)
        
        keyboard = [
            [InlineKeyboardButton(f"📧 Send Gmail ({total_count} left)", callback_data="send_gmail")],
            [InlineKeyboardButton("🔙 Main Menu", callback_data="main_menu")]
        ]
        
        await update.message.reply_text(
            f"✅ Generated {total_count} variations!\nClick below to receive:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    
    elif text and not text.startswith('/'):
        await update.message.reply_text("Please send valid Gmail (e.g., example@gmail.com)")
    
    else:
        keyboard = [
            [InlineKeyboardButton("📧 Gmail Generator", callback_data="main_gmail")],
            [InlineKeyboardButton("🌍 Foreign Names", callback_data="main_foreign")]
        ]
        await update.message.reply_text("Choose service:", reply_markup=InlineKeyboardMarkup(keyboard))

async def callback_query_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    data = query.data

    print(f"DEBUG: Received callback data: {data}")  # Debug line

    try:
        if data == "main_menu":
            await show_main_menu(update, context)
        
        elif data == "main_gmail":
            await main_gmail_handler(update, context)
        
        elif data == "new_gmail":
            await new_gmail_handler(update, context)
        
        elif data == "main_foreign":
            await main_foreign_handler(update, context)
        
        elif data == "send_gmail":
            if user_id not in user_gmail_data:
                await query.edit_message_text("No Gmail data. Send Gmail first.")
                return
            
            variations = user_gmail_data[user_id]["variations"]
            current_index = user_gmail_data[user_id]["current_index"]
            
            if current_index < len(variations):
                variation = variations[current_index]
                await context.bot.send_message(
                    chat_id=query.message.chat_id,
                    text=f"{variation}@gmail.com"
                )
                
                user_gmail_data[user_id]["current_index"] += 1
                remaining = len(variations) - user_gmail_data[user_id]["current_index"]
                
                if remaining > 0:
                    keyboard = [
                        [InlineKeyboardButton(f"📧 Send Gmail ({remaining} left)", callback_data="send_gmail")],
                        [InlineKeyboardButton("🔙 Main Menu", callback_data="main_menu")]
                    ]
                    await query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(keyboard))
                else:
                    await query.edit_message_text("✅ All variations sent!")
                    user_gmail_data[user_id]["current_index"] = 0
        
        # ✅ FIXED: Country selection - SIMPLE AND DIRECT
        elif data in ["saudi", "ecuador", "random"]:
            print(f"DEBUG: Country selected: {data}")  # Debug
            country = data
            names = foreign_data.get(country, [])
            
            if not names:
                await query.edit_message_text("❌ No data found for this country.")
                return
            
            # Store user data
            user_foreign_data[user_id] = {
                "country": country,
                "current_index": 0
            }
            
            # Show first name
            first_name, last_name, tg_username = names[0]
            
            country_names = {
                "saudi": "🇸🇦 Saudi Arabia",
                "ecuador": "🇪🇨 Ecuador", 
                "random": "🌍 Random Names"
            }
            
            keyboard = [
                [InlineKeyboardButton("🔄 Next Name", callback_data="next_foreign")],
                [InlineKeyboardButton("🔙 Back to Countries", callback_data="main_foreign")],
            ]
            
            await query.edit_message_text(
                f"**{country_names[country]}**\n\n"
                f"👤 **Name:** {first_name} {last_name}\n"
                f"📱 **Telegram:** {tg_username}\n\n"
                f"📊 **1/{len(names)}**",
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode='Markdown'
            )
        
        elif data == "next_foreign":
            if user_id not in user_foreign_data:
                await query.edit_message_text("❌ Please select a country first.")
                return
            
            country = user_foreign_data[user_id]["country"]
            names = foreign_data.get(country, [])
            
            if not names:
                await query.edit_message_text("❌ No data found.")
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
                [InlineKeyboardButton("🔄 Next Name", callback_data="next_foreign")],
                [InlineKeyboardButton("🔙 Back to Countries", callback_data="main_foreign")],
            ]
            
            await query.edit_message_text(
                f"**{country_names[country]}**\n\n"
                f"👤 **Name:** {first_name} {last_name}\n"
                f"📱 **Telegram:** {tg_username}\n\n"
                f"📊 **{next_index+1}/{len(names)}**",
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode='Markdown'
            )
            
    except Exception as e:
        print(f"❌ Error in callback: {e}")
        await query.edit_message_text("❌ Error occurred. Please try /start again.")

# Main function
def main():
    keep_alive()
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(callback_query_handler))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    print("🚀 Bot started - FOREIGN NAMES FIXED VERSION")
    app.run_polling()

if __name__ == "__main__":
    main()
