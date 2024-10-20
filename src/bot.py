from aiogram import Bot
from decouple import config
TG_TOKEN = config('TG_TOKEN', default='', cast=str)

if not TG_TOKEN:
    raise ValueError("TG_TOKEN is not set in env!")

BOT_INSTANCE = Bot(token=TG_TOKEN , parse_mode='HTML')
