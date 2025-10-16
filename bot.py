from itertools import product
from threading import Thread
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler,
    MessageHandler, ContextTypes, filters
)
# ✅ এই লাইব্রেরিটি ইম্পোর্ট করা হলো MessageNotModifiedError হ্যান্ডেল করতে
from telegram.error import MessageNotModified
import asyncio

# ✅ Telegram Bot Token
BOT_TOKEN = "8107648163:AAH5pbOD_yjOHdV8yWiN3Zw702bNOl7LmpQ"

# ✅ Flask app for Render
flask_app = Flask(_name_)

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
        ("إبراهيم", "ماجد", "@ibrahim_majed06"),
        ("حسن", "ناصر", "@hasan_nasser07"),
        ("سلمان", "رامي", "@salman_rami08"),
        ("فهد", "خالد", "@fahad_khaled09"),
        ("ناصر", "سعيد", "@nasser_saeed10"),
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
    ]
}

# Global storage for user data
user_gmail_data = {}
user_foreign_data = {}

# Generate ALL possible case variations for Gmail username
def generate_case_variations(username):
    variations = set()
    username_lower = username.lower()
    
    # এটি 2^N ভ্যারিয়েশন তৈরি করে, যা বড় ইউজারনেমের জন্য খুব বেশি হতে পারে।
    for i in range(2 ** len(username_lower)):
        variation = []
        for j, char in enumerate(username_lower):
            if (i >> j) & 1:
                variation.append(char.upper())
            else:
                variation.append(char)
        variations.add(''.join(variation))
    
    return list(variations)

# Fast button handlers - no delays
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    user_name = user.first_name
    
    keyboard = [
        [InlineKeyboardButton("📧 Gmail Generator", callback_data="main_gmail")],
        [InlineKeyboardButton("🌍 Foreign Names", callback_data="main_foreign")]
    ]
    
    await update.message.reply_text(
        f"Hello {user_name}! 👋\nChoose service:", 
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    keyboard = [
        [InlineKeyboardButton("📧 Gmail Generator", callback_data="main_gmail")],
        [InlineKeyboardButton("🌍 Foreign Names", callback_data="main_foreign")]
    ]
    
    await query.edit_message_text("🏠 Main Menu", reply_markup=InlineKeyboardMarkup(keyboard))

async def main_gmail_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    
    if user_id in user_gmail_data and user_gmail_data[user_id]["variations"]:
        variations = user_gmail_data[user_id]["variations"]
        current_index = user_gmail_data[user_id]["current_index"]
        remaining = len(variations) - current_index
        
        if remaining > 0:
            keyboard = [
                [InlineKeyboardButton(f"📧 Send Gmail ({remaining} left)", callback_data="send_gmail")],
                [InlineKeyboardButton("🔄 New Gmail", callback_data="new_gmail")],
                [InlineKeyboardButton("🔙 Main Menu", callback_data="main_menu")]
            ]
            await query.edit_message_text(
                f"📧 Gmail Generator\n{remaining} variations remaining", 
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
            return
    
    keyboard = [[InlineKeyboardButton("🔙 Main Menu", callback_data="main_menu")]]
    await query.edit_message_text(
        "📧 Gmail Generator\nSend your Gmail address:", 
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def new_gmail_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    keyboard = [[InlineKeyboardButton("🔙 Main Menu", callback_data="main_menu")]]
    await query.edit_message_text(
        "📧 New Gmail\nSend your Gmail address:", 
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def main_foreign_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    buttons = [
        [InlineKeyboardButton("🇸🇦 Saudi Arabia", callback_data="saudi")],
        [InlineKeyboardButton("🇪🇨 Ecuador", callback_data="ecuador")],
        [InlineKeyboardButton("🌍 Random Names", callback_data="random")],
        [InlineKeyboardButton("🔙 Main Menu", callback_data="main_menu")]
    ]
    
    await query.edit_message_text("🌍 Foreign Names", reply_markup=InlineKeyboardMarkup(buttons))

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    text = update.message.text.strip()

    if text and not text.startswith('/') and '@gmail.com' in text:
        username = text.split('@')[0].strip()
        
        if not username:
            await update.message.reply_text("Please send valid Gmail address.")
            return
        
        # Generate variations
        variations = generate_case_variations(username)
        
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
            f"✅ Generated {total_count} variations!", 
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
                # নতুন মেসেজ হিসেবে পাঠানো হচ্ছে
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
                    # ✅ MessageNotModifiedError এড়ানো
                    try:
                        await query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(keyboard))
                    except MessageNotModified:
                        pass # যদি রিপ্লাই মার্কআপ একই থাকে তবে উপেক্ষা করা হবে
                else:
                    await query.edit_message_text("✅ All variations sent!")
                    # সবগুলো ভ্যারিয়েশন পাঠানো হলে ইনডেক্স রিসেট করা
                    user_gmail_data[user_id]["current_index"] = 0
        
        # ✅ FAST COUNTRY HANDLERS
        elif data == "saudi":
            names = foreign_data["saudi"]
            first_name, last_name, tg_username = names[0]
            user_foreign_data[user_id] = {"country": "saudi", "current_index": 0}
            
            keyboard = [
                [InlineKeyboardButton("🔄 Next Name", callback_data="next_foreign")],
                [InlineKeyboardButton("🔙 Back", callback_data="main_foreign")],
            ]
            
            await query.edit_message_text(
                f"**🇸🇦 Saudi Arabia**\n\n"
                f"👤 {first_name} {last_name}\n"
                f"📱 {tg_username}\n\n"
                f"1/{len(names)}",
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode='Markdown'
            )
        
        elif data == "ecuador":
            names = foreign_data["ecuador"]
            first_name, last_name, tg_username = names[0]
            user_foreign_data[user_id] = {"country": "ecuador", "current_index": 0}
            
            keyboard = [
                [InlineKeyboardButton("🔄 Next Name", callback_data="next_foreign")],
                [InlineKeyboardButton("🔙 Back", callback_data="main_foreign")],
            ]
            
            await query.edit_message_text(
                f"**🇪🇨 Ecuador**\n\n"
                f"👤 {first_name} {last_name}\n"
                f"📱 {tg_username}\n\n"
                f"1/{len(names)}",
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode='Markdown'
            )
        
        elif data == "random":
            names = foreign_data["random"]
            first_name, last_name, tg_username = names[0]
            user_foreign_data[user_id] = {"country": "random", "current_index": 0}
            
            keyboard = [
                [InlineKeyboardButton("🔄 Next Name", callback_data="next_foreign")],
                [InlineKeyboardButton("🔙 Back", callback_data="main_foreign")],
            ]
            
            await query.edit_message_text(
                f"**🌍 Random Names**\n\n"
                f"👤 {first_name} {last_name}\n"
                f"📱 {tg_username}\n\n"
                f"1/{len(names)}",
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode='Markdown'
            )
        
        elif data == "next_foreign":
            if user_id not in user_foreign_data:
                await query.edit_message_text("Please select country first.")
                return
            
            country = user_foreign_data[user_id]["country"]
            names = foreign_data[country]
            
            current_index = user_foreign_data[user_id]["current_index"]
            next_index = (current_index + 1) % len(names)
            user_foreign_data[user_id]["current_index"] = next_index
            
            first_name, last_name, tg_username = names[next_index]
            
            country_names = {"saudi": "🇸🇦 Saudi Arabia", "ecuador": "🇪🇨 Ecuador", "random": "🌍 Random Names"}
            
            keyboard = [
                [InlineKeyboardButton("🔄 Next Name", callback_data="next_foreign")],
                [InlineKeyboardButton("🔙 Back", callback_data="main_foreign")],
            ]
            
            # ✅ MessageNotModifiedError এড়ানো
            try:
                await query.edit_message_text(
                    f"**{country_names[country]}**\n\n"
                    f"👤 {first_name} {last_name}\n"
                    f"📱 {tg_username}\n\n"
                    f"{next_index+1}/{len(names)}",
                    reply_markup=InlineKeyboardMarkup(keyboard),
                    parse_mode='Markdown'
                )
            except MessageNotModified:
                pass # যদি মেসেজের টেক্সট বা মার্কআপ একই থাকে তবে উপেক্ষা করা হবে
            
    # ✅ MessageNotModifiedError কে আলাদাভাবে হ্যান্ডেল করা হলো
    except MessageNotModified:
        # এটি প্রায়ই ঘটে যখন দ্রুত ক্লিক করা হয়, ইউজারকে কোনো বার্তা না দেখিয়ে এড়িয়ে যাওয়া যেতে পারে।
        pass
    except Exception as e:
        # অন্য কোনো গুরুত্বপূর্ণ ত্রুটি হলে ইউজারকে জানানো
        await query.edit_message_text("❌ An error occurred. Please try /start again.")

# Main function - optimized for Render
def main():
    keep_alive()
    
    # Fast bot configuration
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    
    # Add handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(callback_query_handler))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    print("🚀 FAST BOT STARTED - OPTIMIZED FOR RENDER")
    app.run_polling(drop_pending_updates=True)  # Faster startup

if _name_ == "_main_":
    main()
