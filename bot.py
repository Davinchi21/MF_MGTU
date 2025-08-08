import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# Папка с файлами
FILES_DIR = 'files'

# Названия кнопок и соответствующие имена файлов
FILE_BUTTONS = {
    "📄 Документ 1": "file1.pdf",
    "📝 Документ 2": "file2.docx",
    "📊 Таблица": "file3.xlsx"
}

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton(text=btn_text, callback_data=filename)]
        for btn_text, filename in FILE_BUTTONS.items()
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Выберите нужный файл:", reply_markup=reply_markup)

# Обработка кнопок
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    file_name = query.data
    file_path = os.path.join(FILES_DIR, file_name)

    if os.path.exists(file_path):
        await query.message.reply_document(document=open(file_path, 'rb'))
    else:
        await query.message.reply_text("Файл не найден.")

# Запуск бота
def main():
    TOKEN = "TOKEN_BOT"  # Замени на свой токен

    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()
