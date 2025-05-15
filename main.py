import asyncio
from aiogram import Bot, Dispatcher, types, F
from core.handlers.basic import get_start, add_tasks, user_list, done_number, delete_task, clear_tasks
import logging
from id import TOKEN
from aiogram.filters import Command
from id import bot, dp
from core.handlers.callback import get_callback_inli






async def start():
    dp.message.register(get_start, Command(commands=['start']))# запуск бота после команды старт

    dp.message.register(add_tasks, Command(commands=['add']))
    dp.message.register(user_list, Command(commands=['list']))
    dp.message.register(done_number, Command(commands=['done']))
    dp.message.register(delete_task, Command(commands=['delete']))
    dp.message.register(clear_tasks, Command(commands=['clear']))


    try:
       await dp.start_polling(bot)
    finally:
        await bot.session.close()




if __name__ == '__main__':
    print('bot start')
    asyncio.run(start())
