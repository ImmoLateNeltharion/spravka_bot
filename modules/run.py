import asyncio

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config.config import BOT_TOKEN

bot = Bot(BOT_TOKEN, parse_mode="HTML")
loop = asyncio.get_event_loop()
storage = MemoryStorage()
dp = Dispatcher(bot, loop=loop, storage=storage)
