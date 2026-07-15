import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
import worker
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

API_TOKEN = os.getenv("API_TOKEN")
if not API_TOKEN:
    raise ValueError("API_TOKEN not set in environment variables")

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

accounts = []

def main_menu():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("➕ Добавить аккаунт", callback_data="add"))
    kb.add(InlineKeyboardButton("▶️ Запустить скрипт", callback_data="start"))
    kb.add(InlineKeyboardButton("⏹ Остановить скрипт", callback_data="stop"))
    return kb

@dp.message_handler(commands=['start'])
async def start_cmd(message: types.Message):
    logger.info(f"Start command from user {message.from_user.id}")
    await message.answer("Меню управления:", reply_markup=main_menu())

@dp.callback_query_handler(lambda c: c.data == "add")
async def add_account(callback: types.CallbackQuery):
    if len(accounts) >= 5:
        await callback.message.answer("Максимум 5 аккаунтов!")
        await callback.answer()
        return
    await callback.message.answer("Отправь имя для новой сессии:")
    await callback.answer()

@dp.callback_query_handler(lambda c: c.data == "start")
async def start_script(callback: types.CallbackQuery):
    logger.info("Starting all accounts")
    await callback.message.answer("Запускаю все аккаунты...")
    await callback.answer()
    try:
        await worker.start_all(accounts)
    except Exception as e:
        logger.error(f"Error starting accounts: {e}")
        await callback.message.answer(f"Ошибка: {str(e)}")

@dp.callback_query_handler(lambda c: c.data == "stop")
async def stop_script(callback: types.CallbackQuery):
    logger.info("Stopping all accounts")
    await callback.message.answer("Останавливаю все аккаунты...")
    await callback.answer()
    try:
        await worker.stop_all()
    except Exception as e:
        logger.error(f"Error stopping accounts: {e}")
        await callback.message.answer(f"Ошибка: {str(e)}")

if __name__ == "__main__":
    logger.info("Bot starting...")
    executor.start_polling(dp, skip_updates=True)