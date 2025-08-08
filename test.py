import os
from urllib.parse import quote, unquote
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = "TOKEN_BOT"
ROOT_DIR = "library"  # Папка, где хранится "МФ МГТУ"

# Функция генерации клавиатуры для папки
def build_keyboard(current_path: str):
    abs_path = os.path.join(ROOT_DIR, current_path)
    entries = os.listdir(abs_path)
    entries.sort()

    keyboard = []
    for entry in entries:
        full_entry_path = os.path.join(abs_path, entry)
        encoded_path = quote(os.path.join(current_path, entry))
        if os.path.isdir(full_entry_path):
            keyboard.append([InlineKeyboardButton(f"📁 {entry}", callback_data=f"nav|{encoded_path}")])
        else:
            keyboard.append([InlineKeyboardButton(f"📄 {entry}", callback_data=f"file|{encoded_path}")])

    # Назад
    if current_path:
        parent_path = os.path.dirname(current_path)
        encoded_parent = quote(parent_path)
        keyboard.append([InlineKeyboardButton("⬅️ Назад", callback_data=f"nav|{encoded_parent}")])

    return InlineKeyboardMarkup(keyboard)

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = build_keyboard("")
    await update.message.reply_text("📚 Выберите папку:", reply_markup=keyboard)

# Обработка нажатий
async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data.startswith("nav|"):
        path = unquote(data[4:])
        keyboard = build_keyboard(path)
        await query.edit_message_text(f"📁 Папка: `{path or 'МФ МГТУ'}`", parse_mode="Markdown", reply_markup=keyboard)

    elif data.startswith("file|"):
        rel_path = unquote(data[5:])
        abs_path = os.path.join(ROOT_DIR, rel_path)

        if os.path.isfile(abs_path):
            try:
                await query.message.reply_document(document=open(abs_path, "rb"))
            except Exception as e:
                await query.message.reply_text(f"❌ Ошибка при отправке файла:\n{e}")
        else:
            await query.message.reply_text("❌ Это не файл.")

# Запуск бота
def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_callback))
    app.run_polling()

if __name__ == "__main__":
    main()
