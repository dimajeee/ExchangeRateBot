import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext
from sqlalchemy.orm import sessionmaker
from db.database import get_db
from services import save_user_name, get_user_name
from utils.currency import get_currency_rate
from dotenv import load_dotenv
import os

logging.basicConfig(level=logging.INFO)

ASK_NAME, SHOW_CURRENCY = range(2)

def start(update: Update, context: CallbackContext):
    """Обработка команды /start, начало диалога."""
    update.message.reply_text(
        "Привет! Как тебя зовут?"
    )
    return ASK_NAME

def ask_name(update: Update, context: CallbackContext):
    """Обработка получения имени и переход к следующему состоянию."""
    user_name = update.message.text
    db = next(get_db())
    save_user_name(update.message.from_user.id, user_name, db)
    
    update.message.reply_text(
        f"Приятно познакомиться, {user_name}! Теперь можешь узнать курс валют, введи /currency."
    )
    
    return SHOW_CURRENCY

def show_currency(update: Update, context: CallbackContext):
    """Обработка команды /currency и показ курса валют."""
    db = next(get_db())
    user_name = get_user_name(update.message.from_user.id, db)
    
    if not user_name:
        update.message.reply_text("Сначала представьтесь с помощью команды /start.")
        return ConversationHandler.END

    rates = get_currency_rate()
    update.message.reply_text(
        f"Привет, {user_name}!\nТекущий курс валют:\nUSD: {rates['USD']} RUB\nEUR: {rates['EUR']} RUB"
    )
    
    return ConversationHandler.END

def cancel(update: Update, context: CallbackContext):
    """Отмена диалога."""
    update.message.reply_text("Диалог отменён. До свидания!")
    return ConversationHandler.END

def main():

    load_dotenv()
    TOKEN = os.getenv("TOKEN_BOT")

    updater = Updater(TOKEN, use_context=True)
    
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            ASK_NAME: [MessageHandler(Filters.text & ~Filters.command, ask_name)],
            SHOW_CURRENCY: [CommandHandler('currency', show_currency)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
