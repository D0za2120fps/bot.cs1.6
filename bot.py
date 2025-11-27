# bot.py
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters
from config import ADMIN_ID, BOT_TOKEN, PRIVILEGES
from utils.password_gen import generate_password
from utils.ticket_system import TicketSystem
from utils.ftp_handler import FTPHandler
from utils.rcon_handler import RCONHandler
from keep_alive import keep_alive
keep_alive()

# Настройка логов
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Инициализация систем
tickets = TicketSystem()
ftp = FTPHandler()
rcon = RCONHandler()

# Главное меню
def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    keyboard = [
        [InlineKeyboardButton("🛒 Купить привилегию", callback_data='buy')],
        [InlineKeyboardButton("📜 Мои покупки", callback_data='my_tickets')],
        [InlineKeyboardButton("💬 Поддержка", callback_data='support')],
        [InlineKeyboardButton("ℹ Информация о сервере", callback_data='info')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(f"Привет, {user.first_name}! 👋\nВыберите действие:", reply_markup=reply_markup)

# Обработка кнопок меню
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    if query.data == 'buy':
        keyboard = [[InlineKeyboardButton(p + " 💎", callback_data=f'buy_{p}')] for p in PRIVILEGES.keys()]
        await query.edit_message_text("Выберите привилегию:", reply_markup=InlineKeyboardMarkup(keyboard))
    elif query.data.startswith('buy_'):
        privilege = query.data.split('_')[1]
        context.user_data['privilege'] = privilege
        await query.edit_message_text(f"Вы выбрали: {privilege} 🎯\nВведите срок действия: 7 / 30 / forever дней")
    elif query.data == 'my_tickets':
        tickets_list = tickets.get_user_tickets(user_id)
        if not tickets_list:
            await query.edit_message_text("У вас пока нет активных покупок. 🕒")
        else:
            msg = "Ваши покупки:\n\n" + "\n".join([str(t) for t in tickets_list])
            await query.edit_message_text(msg)
    elif query.data == 'support':
        await query.edit_message_text("Свяжитесь с администратором: " + ADMIN_ID)
    elif query.data == 'info':
        await query.edit_message_text("Сервер CS 1.6 JailBreak 🕹\nIP: ...\nПроверяйте онлайн!")

# Обработка текстовых сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text

    if 'privilege' in context.user_data and 'duration' not in context.user_data:
        # пользователь ввёл срок
        if text in ['7', '30', 'forever']:
            context.user_data['duration'] = text
            await update.message.reply_text("Введите ваш ник на сервере 🎮")
        else:
            await update.message.reply_text("Пожалуйста, введите корректный срок: 7 / 30 / forever")
    elif 'duration' in context.user_data and 'nick' not in context.user_data:
        # пользователь ввёл ник
        context.user_data['nick'] = text
        password = generate_password()
        context.user_data['password'] = password
        await update.message.reply_text(f"Ваш пароль для setinfo:\n`setinfo _pw \"{password}\"` 🔑\n\nОтправьте скрин перевода для подтверждения оплаты 💳", parse_mode='Markdown')
        # Создать тикет
        tickets.create_ticket(user_id, context.user_data)
    elif update.message.photo:
        # пользователь прислал скрин
        ticket_id = tickets.find_ticket_by_user(user_id)
        if ticket_id:
            tickets.attach_screenshot(ticket_id, update.message.photo[-1].file_id)
            await update.message.reply_text("Скрин получен! 🖼\nАдминистратор проверит оплату и подтвердит ✅")
        else:
            await update.message.reply_text("Нет активного тикета. Сначала выберите привилегию 🛒")
    else:
        await update.message.reply_text("Я не понимаю это сообщение. Используйте меню ⬇️")

# Запуск бота
if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(MessageHandler(filters.TEXT | filters.PHOTO, handle_message))
    print("🤖 Бот запущен!")
    app.run_polling()
