from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
import asyncio
import logging

from config.config import load_env, Config
from database.postgres import Database
from middlewares.outer.outer_middlewares import MainOuterMiddleware
from handlers.registation_handler import registration_router

logger = logging.getLogger(__name__)

async def main() -> None:
    logging.basicConfig(
         level=logging.INFO, format='%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s')
    logger.info('Starting bot...')

    config: Config = load_env('.env')
    storage = MemoryStorage()

    bot = Bot(token=config.TGBot.token)
    dp = Dispatcher(storage=storage)

    database: Database = Database()

    # Middlewares
    dp.update.outer_middleware(MainOuterMiddleware(db=database))

    # Routers
    dp.include_router(registration_router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())