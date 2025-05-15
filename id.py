from aiogram import Dispatcher, Bot

TOKEN='YOUR_TOKEN'

bot = Bot(token=TOKEN)  # pars_mode для настройки дизайна текста
dp = Dispatcher(bot=bot)