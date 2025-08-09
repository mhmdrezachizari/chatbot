import os
import base64
from telegram import Update, File
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters
from openai import OpenAI
from dotenv import load_dotenv
from database import save_user, save_message, save_image

load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
LIARA_API_KEY = os.getenv("LIARA_API_KEY")
BASE_URL = os.getenv("BASE_URL")

client = OpenAI(
    base_url=BASE_URL,
    api_key=LIARA_API_KEY,
)

async def ask_gpt(message: str) -> str:
    try:
        response = client.chat.completions.create(
            model="google/gemini-2.0-flash-001",
            messages=[{"role": "user", "content": message}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f" خطا: {str(e)}"

async def ask_gpt_with_image(image_base64: str) -> str:
    """
    ارسال تصویر به GPT-4 Vision و دریافت پاسخ
    """
    try:
        response = client.chat.completions.create(
            model="openai/o4-mini",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "لطفاً این تصویر را تحلیل کن."},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_base64}"
                            }
                        }
                    ]
                }
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f" خطا در تحلیل تصویر: {str(e)}"


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
 <b>خوش آمدی {user.first_name} عزیز!</b>

 تو اولین باره که با ربات صحبت می‌کنی، اطلاعاتت ذخیره شد 
"""
    else:
        message = f"""
👋 <b>خوش برگشتی {user.first_name}!</b>
هرچی میخواهی از هوش مصنوعی بپرس
"""

    await update.message.reply_text(message, parse_mode="HTML")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    msg = update.message.text.strip()

    if not msg:
        await update.message.reply_text(" لطفاً یک پیام معتبر ارسال کن.")
        return

    save_message(user.id, msg)

    temp_message = await update.message.reply_text("⏳ در حال دریافت پاسخ از هوش مصنوعی...")

    try:
        reply = await ask_gpt(msg)
    except Exception as e:
        reply = " خطا در پاسخ‌دهی: " + str(e)

    try:
        await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=temp_message.message_id)
    except:
        pass

    await update.message.reply_text(reply)


async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    photo = update.message.photo[-1] 
    file: File = await context.bot.get_file(photo.file_id)

    image_bytes = await file.download_as_bytearray()

    image_base64 = base64.b64encode(image_bytes).decode()

    saved = save_image(user.id, image_base64)
    if not saved:
        await update.message.reply_text(" خطا در ذخیره عکس در دیتابیس.")
        return

    save_message(user.id, "[تصویر ارسال شد]")

    temp_message = await update.message.reply_text("⏳ در حال تحلیل تصویر توسط هوش مصنوعی...")

    try:
        reply = await ask_gpt_with_image(image_base64)
    except Exception as e:
        reply = " خطا در پاسخ‌دهی به تصویر: " + str(e)

    try:
        await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=temp_message.message_id)
    except:
        pass

    await update.message.reply_text(reply)


if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    print(" ربات در حال اجراست...")
    app.run_polling()
