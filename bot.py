# bot.py
import os
import re
import itertools
import random
import io
from telegram import (
    Update, InlineKeyboardButton, InlineKeyboardMarkup
)
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    CallbackQueryHandler, filters, ContextTypes
)

# Token: পরিবেশ ভেরিয়েবল থেকে নাও (secure). নচেৎ এখানে বসিয়ে দিবে:
BOT_TOKEN = os.getenv("BOT_TOKEN", "# bot.py
import os
import re
import itertools
import random
import io
from telegram import (
    Update, InlineKeyboardButton, InlineKeyboardMarkup
)
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    CallbackQueryHandler, filters, ContextTypes
)

# Token: পরিবেশ ভেরিয়েবল থেকে নাও (secure). নচেৎ এখানে বসিয়ে দিবে:
BOT_TOKEN = os.getenv("BOT_TOKEN", "REPLACE_WITH_YOUR_TOKEN")

# --- Utility: split email ---
def split_email(email: str):
    email = email.strip()
    m = re.match(r'^([^@]+)@([^\s@]+\.[^\s@]+)$', email)
    if not m:
        return None, None
    return m.group(1), m.group(2)

# --- Generate case-only variants ---
def generate_case_variants(local: str, domain: str, count: int):
    """
    Only toggles letters' case. Numbers/symbols unchanged.
    Returns up to `count` variants (strings like local@domain).
    Strategy:
     - If total possible (2^k) <= count -> produce all.
     - If small k -> sample masks with step.
     - If large k -> random sample masks until we have `count`.
    """
    chars = list(local)
    alpha_idx = [i for i,ch in enumerate(chars) if ch.isalpha()]
    k = len(alpha_idx)

    # trivial case: no letters
    if k == 0:
        return [f"{local}@{domain}"]

    total = 1 << k  # 2^k

    def variant_from_mask(mask):
        out = chars[:]
        for j, idx in enumerate(alpha_idx):
            if (mask >> j) & 1:
                out[idx] = out[idx].upper()
            else:
                out[idx] = out[idx].lower()
        return "".join(out) + "@" + domain

    results = []
    seen = set()

    # include original as first
    orig = variant_from_mask(0)
    results.append(orig)
    seen.add(orig)

    # if requested >= total, produce all
    if count >= total:
        for mask in range(1, total):
            v = variant_from_mask(mask)
            results.append(v)
            if len(results) >= count:
                break
        return results[:count]

    # if total not big (k small), sample deterministically
    if k <= 22:  # 2^22 = 4,194,304 manageable for stepping
        step = max(1, total // count)
        mask = 1
        while len(results) < count and mask < total:
            v = variant_from_mask(mask)
            if v not in seen:
                seen.add(v); results.append(v)
            mask += step
        # if still short, fill sequentially
        mask2 = 1
        while len(results) < count and mask2 < total:
            v = variant_from_mask(mask2)
            if v not in seen:
                seen.add(v); results.append(v)
            mask2 += 1
        return results[:count]

    # for large k: random sample masks
    rnd = random.Random()
    attempts = 0
    max_attempts = count * 20  # safety cap
    while len(results) < count and attempts < max_attempts:
        mask = rnd.getrandbits(k)
        v = variant_from_mask(mask)
        if v not in seen:
            seen.add(v); results.append(v)
        attempts += 1

    # fallback: if still fewer, try a limited deterministic sweep of lower bits
    if len(results) < count:
        base = 1 << 22
        mask = 1
        while len(results) < count and mask < base:
            v = variant_from_mask(mask)
            if v not in seen:
                seen.add(v); results.append(v)
            mask += 1

    return results[:count]


# --- Handlers ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # reset user state
    context.user_data.clear()
    await update.message.reply_text(
        "👋 হাই! আপনার জিমেইল সেন্ড করুন (উদাহরণ: valothakuk58@gmail.com)\n\n"
        "আমি কেবল অক্ষরগুলোর বড়/ছোট বদল করে ভ্যারিয়েন্ট তৈরি করবো — সংখ্যা/ডট/প্লাস কিছুই বদলাবো না।"
    )

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    local, domain = split_email(text)
    if not local:
        await update.message.reply_text("❌ ভুল ইমেইল ফরম্যাট। অনুগ্রহ করে সঠিক Gmail দিন (উদাহরণ: valothakuk58@gmail.com).")
        return

    # আমরা Gmail প্রাথমিকভাবে ধরবো — চাইলে পরিবর্তন করা যায়
    if domain.lower() != "gmail.com" and domain.lower() != "googlemail.com":
        await update.message.reply_text("⚠️ এই বট মূলত Gmail ঠিকানার জন্য। অনুগ্রহ করে Gmail (example@gmail.com) পাঠান.")
        return

    # store
    context.user_data['local'] = local
    context.user_data['domain'] = domain.lower()

    # Inline buttons for counts
    kb = [
        [InlineKeyboardButton("100", callback_data="count_100"),
         InlineKeyboardButton("200", callback_data="count_200")],
        [InlineKeyboardButton("500", callback_data="count_500"),
         InlineKeyboardButton("1000", callback_data="count_1000")],
        [InlineKeyboardButton("Cancel", callback_data="cancel")]
    ]
    await update.message.reply_text(
        f"📧 পাওয়া গেল: `{local}@{domain}`\nকতটি ভ্যারিয়েন্ট চান? (নীচের বাটন বেছে নিন)",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(kb)
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()  # acknowledge
    data = query.data

    if data == "cancel":
        context.user_data.clear()
        await query.edit_message_text("❌ অপারেশন বাতিল করা হলো। /start দিয়ে আবার শুরু করুন।")
        return

    # extract count
    try:
        count = int(data.split("_",1)[1])
    except:
        await query.edit_message_text("⚠️ অনিচ্ছিত অপশন। /start দিয়ে আবার চেষ্টা করুন।")
        return

    local = context.user_data.get('local')
    domain = context.user_data.get('domain')
    if not local:
        await query.edit_message_text("🛈 প্রথমে /start করে তোমার জিমেইল দাও।")
        return

    # update the message to show progress
    await query.edit_message_text(f"⏳ Generating {count} variants for `{local}@{domain}` ...", parse_mode="Markdown")

    # generate variants
    variants = generate_case_variants(local, domain, count)

    # If many results, send as file to avoid long chat
    if len(variants) > 200:
        content = "\n".join(variants)
        bio = io.BytesIO(content.encode("utf-8"))
        bio.name = f"variants_{local}_{count}.txt"
        await context.bot.send_document(chat_id=query.message.chat_id, document=bio)
        await context.bot.send_message(chat_id=query.message.chat_id, text=f"✅ {len(variants)} ভ্যারিয়েন্ট ডাউনলোড-ফাইলে পাঠানো হয়েছে।")
    else:
        chunk_size = 40
        for i in range(0, len(variants), chunk_size):
            chunk = variants[i:i+chunk_size]
            await context.bot.send_message(chat_id=query.message.chat_id, text="\n".join(chunk))

    # clear user state
    context.user_data.clear()

# --- Main run ---
def main():
    if BOT_TOKEN.startswith("REPLACE") or not BOT_TOKEN:
        print("ERROR: Set BOT_TOKEN as environment variable or edit bot.py to include your token.")
        return

    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.add_handler(CallbackQueryHandler(button_handler))
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
")

# --- Utility: split email ---
def split_email(email: str):
    email = email.strip()
    m = re.match(r'^([^@]+)@([^\s@]+\.[^\s@]+)$', email)
    if not m:
        return None, None
    return m.group(1), m.group(2)

# --- Generate case-only variants ---
def generate_case_variants(local: str, domain: str, count: int):
    """
    Only toggles letters' case. Numbers/symbols unchanged.
    Returns up to `count` variants (strings like local@domain).
    Strategy:
     - If total possible (2^k) <= count -> produce all.
     - If small k -> sample masks with step.
     - If large k -> random sample masks until we have `count`.
    """
    chars = list(local)
    alpha_idx = [i for i,ch in enumerate(chars) if ch.isalpha()]
    k = len(alpha_idx)

    # trivial case: no letters
    if k == 0:
        return [f"{local}@{domain}"]

    total = 1 << k  # 2^k

    def variant_from_mask(mask):
        out = chars[:]
        for j, idx in enumerate(alpha_idx):
            if (mask >> j) & 1:
                out[idx] = out[idx].upper()
            else:
                out[idx] = out[idx].lower()
        return "".join(out) + "@" + domain

    results = []
    seen = set()

    # include original as first
    orig = variant_from_mask(0)
    results.append(orig)
    seen.add(orig)

    # if requested >= total, produce all
    if count >= total:
        for mask in range(1, total):
            v = variant_from_mask(mask)
            results.append(v)
            if len(results) >= count:
                break
        return results[:count]

    # if total not big (k small), sample deterministically
    if k <= 22:  # 2^22 = 4,194,304 manageable for stepping
        step = max(1, total // count)
        mask = 1
        while len(results) < count and mask < total:
            v = variant_from_mask(mask)
            if v not in seen:
                seen.add(v); results.append(v)
            mask += step
        # if still short, fill sequentially
        mask2 = 1
        while len(results) < count and mask2 < total:
            v = variant_from_mask(mask2)
            if v not in seen:
                seen.add(v); results.append(v)
            mask2 += 1
        return results[:count]

    # for large k: random sample masks
    rnd = random.Random()
    attempts = 0
    max_attempts = count * 20  # safety cap
    while len(results) < count and attempts < max_attempts:
        mask = rnd.getrandbits(k)
        v = variant_from_mask(mask)
        if v not in seen:
            seen.add(v); results.append(v)
        attempts += 1

    # fallback: if still fewer, try a limited deterministic sweep of lower bits
    if len(results) < count:
        base = 1 << 22
        mask = 1
        while len(results) < count and mask < base:
            v = variant_from_mask(mask)
            if v not in seen:
                seen.add(v); results.append(v)
            mask += 1

    return results[:count]


# --- Handlers ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # reset user state
    context.user_data.clear()
    await update.message.reply_text(
        "👋 হাই! আপনার জিমেইল সেন্ড করুন (উদাহরণ: valothakuk58@gmail.com)\n\n"
        "আমি কেবল অক্ষরগুলোর বড়/ছোট বদল করে ভ্যারিয়েন্ট তৈরি করবো — সংখ্যা/ডট/প্লাস কিছুই বদলাবো না।"
    )

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    local, domain = split_email(text)
    if not local:
        await update.message.reply_text("❌ ভুল ইমেইল ফরম্যাট। অনুগ্রহ করে সঠিক Gmail দিন (উদাহরণ: valothakuk58@gmail.com).")
        return

    # আমরা Gmail প্রাথমিকভাবে ধরবো — চাইলে পরিবর্তন করা যায়
    if domain.lower() != "gmail.com" and domain.lower() != "googlemail.com":
        await update.message.reply_text("⚠️ এই বট মূলত Gmail ঠিকানার জন্য। অনুগ্রহ করে Gmail (example@gmail.com) পাঠান.")
        return

    # store
    context.user_data['local'] = local
    context.user_data['domain'] = domain.lower()

    # Inline buttons for counts
    kb = [
        [InlineKeyboardButton("100", callback_data="count_100"),
         InlineKeyboardButton("200", callback_data="count_200")],
        [InlineKeyboardButton("500", callback_data="count_500"),
         InlineKeyboardButton("1000", callback_data="count_1000")],
        [InlineKeyboardButton("Cancel", callback_data="cancel")]
    ]
    await update.message.reply_text(
        f"📧 পাওয়া গেল: `{local}@{domain}`\nকতটি ভ্যারিয়েন্ট চান? (নীচের বাটন বেছে নিন)",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(kb)
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()  # acknowledge
    data = query.data

    if data == "cancel":
        context.user_data.clear()
        await query.edit_message_text("❌ অপারেশন বাতিল করা হলো। /start দিয়ে আবার শুরু করুন।")
        return

    # extract count
    try:
        count = int(data.split("_",1)[1])
    except:
        await query.edit_message_text("⚠️ অনিচ্ছিত অপশন। /start দিয়ে আবার চেষ্টা করুন।")
        return

    local = context.user_data.get('local')
    domain = context.user_data.get('domain')
    if not local:
        await query.edit_message_text("🛈 প্রথমে /start করে তোমার জিমেইল দাও।")
        return

    # update the message to show progress
    await query.edit_message_text(f"⏳ Generating {count} variants for `{local}@{domain}` ...", parse_mode="Markdown")

    # generate variants
    variants = generate_case_variants(local, domain, count)

    # If many results, send as file to avoid long chat
    if len(variants) > 200:
        content = "\n".join(variants)
        bio = io.BytesIO(content.encode("utf-8"))
        bio.name = f"variants_{local}_{count}.txt"
        await context.bot.send_document(chat_id=query.message.chat_id, document=bio)
        await context.bot.send_message(chat_id=query.message.chat_id, text=f"✅ {len(variants)} ভ্যারিয়েন্ট ডাউনলোড-ফাইলে পাঠানো হয়েছে।")
    else:
        chunk_size = 40
        for i in range(0, len(variants), chunk_size):
            chunk = variants[i:i+chunk_size]
            await context.bot.send_message(chat_id=query.message.chat_id, text="\n".join(chunk))

    # clear user state
    context.user_data.clear()

# --- Main run ---
def main():
    if BOT_TOKEN.startswith("REPLACE") or not BOT_TOKEN:
        print("ERROR: Set BOT_TOKEN as environment variable or edit bot.py to include your token.")
        return

    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.add_handler(CallbackQueryHandler(button_handler))
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
