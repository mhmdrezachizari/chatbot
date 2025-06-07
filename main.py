import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters
from openai import OpenAI
from dotenv import load_dotenv
from database import save_user, save_message

load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
LIARA_API_KEY = os.getenv("LIARA_API_KEY")

client = OpenAI(
    base_url="https://ai.liara.ir/api/v1/683c9721546d7d2829e0a42d",
    api_key=LIARA_API_KEY,
)

async def ask_gpt(message: str) -> str:
    try:
        response = client.chat.completions.create(
            model="openai/gpt-4o-mini",
            messages=[{"role": "user", "content": message}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ خطا: {str(e)}"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    new_user = save_user(
        user_id=user.id,
        first_name=user.first_name,
        last_name=user.last_name or "",
        username=user.username or "",
        language=user.language_code or "unknown"
    )

    if new_user:
        message = f"""
🎉 <b>خوش آمدی {user.first_name} عزیز!</b>

🧠 تو اولین باره که با ربات صحبت می‌کنی، اطلاعاتت ذخیره شد ✅
"""
    else:
        message = f"""
👋 <b>خوش برگشتی {user.first_name}!</b>
هرچی میخواهی از  هوش مصنوعی بپرس
"""

    await update.message.reply_text(message, parse_mode="HTML")


# async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     user = update.message.from_user
#     user_id = user.id
#     user_message = update.message.text.strip()

#     if not user_message:
#         await update.message.reply_text("لطفاً یک پیام معتبر ارسال کنید.")
#         return

#     save_message(user_id, user_message)

#     reply = await ask_gpt(user_message)
#     await update.message.reply_text(reply)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    msg = update.message.text.strip()

    if not msg:
        await update.message.reply_text("❗ لطفاً یک پیام معتبر ارسال کن.")
        return

    # ذخیره در دیتابیس
    save_message(user.id, msg)

    # ارسال پیام موقت
    temp_message = await update.message.reply_text("⏳ در حال دریافت پاسخ از هوش مصنوعی...")

    try:
        # دریافت پاسخ از GPT
        reply = await ask_gpt(msg)
    except Exception as e:
        reply = "❌ خطا در پاسخ‌دهی: " + str(e)

    # حذف پیام موقت
    try:
        await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=temp_message.message_id)
    except:
        pass  # اگر حذف نشد مشکلی نیست

    # ارسال پاسخ نهایی
    await update.message.reply_text(reply)


if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("✅ ربات در حال اجراست...")
    app.run_polling()
