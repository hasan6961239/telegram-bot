import pandas as pd
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

# تحميل ملف Excel (تأكد من أن الملف موجود في نفس مجلد البوت)
df = pd.read_excel("data.xlsx")  # تأكد أن اسمه data.xlsx

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message.text.strip()
    print("Message received:", message)

    try:
        # إذا كانت الرسالة أرقام فقط، اعتبرها رقم وطني
        if message.isdigit():
            result = df[df['data'] == int(message)]
            if not result.empty:
                await update.message.reply_text(f"الاسم: {result.iloc[0]['name']}")
            else:
                await update.message.reply_text("لم يتم العثور على هذا الرقم الوطني.")
        else:
            # إذا كانت نص، اعتبرها اسم
            result = df[df['name'] == message]
            if not result.empty:
                await update.message.reply_text(f"الرقم الوطني: {result.iloc[0]['data']}")
            else:
                await update.message.reply_text("لم يتم العثور على هذا الاسم.")
    except Exception as e:
        await update.message.reply_text(f"حدث خطأ أثناء البحث: {str(e)}")

# 🔐 ضع هنا التوكن الخاص بك
TOKEN = "8152987163:AAHDytXNSRWEO4_CCYUR1hpvkgwOrLFccTY"

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle))

print("✅ Bot is running...")
app.run_polling()