import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
import worker
import os

API_TOKEN = os.getenv("API_TOKEN")  # токен бота из переменных Railway

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

accounts = []  # список имён сессий

def main_menu():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("➕ Добавить аккаунт", callback_data="add"))
    kb.add(InlineKeyboardButton("▶️ Запустить скрипт", callback_data="start"))
    kb.add(InlineKeyboardButton("⏹ Остановить скрипт", callback_data="stop"))
    return kb

@dp.message_handler(commands=['start'])
async def start_cmd(message: types.Message):
    await message.answer("Меню управления:", reply_markup=main_menu())

@dp.callback_query_handler(lambda c: c.data == "add")
async def add_account(callback: types.CallbackQuery):
    if len(accounts) >= 5:
        await callback.message.answer("Максимум 5 аккаунтов!")
        return
    await callback.message.answer("Отправь имя для новой сессии:")
    # тут можно реализовать ввод имени и запуск авторизации Telethon
    # например: accounts.append(name)

@dp.callback_query_handler(lambda c: c.data == "start")
async def start_script(callback: types.CallbackQuery):
    await callback.message.answer("Запускаю все аккаунты...")
    await worker.start_all(accounts)

@dp.callback_query_handler(lambda c: c.data == "stop")
async def stop_script(callback: types.CallbackQuery):
    await callback.message.answer("Останавливаю все аккаунты...")
    await worker.stop_all()

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)