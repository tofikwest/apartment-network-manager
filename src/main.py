import logging
import asyncio
from aiohttp import web
from decouple import config
from bot import BOT_INSTANCE
from aiogram import Dispatcher
from router import router

PORT= config('PORT', default=5000, cast=int)
HOST = config('HOST', default='0.0.0.0', cast=str)
MODE = config('MODE', default='dev', cast=str)

if MODE == 'dev': PORT = 5001


async def main():
    app = web.Application()
    dispatcher = Dispatcher()
    dispatcher.include_router(router)

    # Print startup information
    logging.info(f"Starting bot in {MODE} mode")
    logging.info(f"Server running on {HOST}:{PORT}")

    processes = [
        web._run_app(app, host=HOST, port=PORT),
        dispatcher.start_polling(BOT_INSTANCE)
    ]

    await asyncio.gather(*processes)

if __name__ == "__main__":
    logging.info('Initializing bot...')
    asyncio.run(main())
