import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import Config, load_config
from src.handlers import stateHandler
from src.models.db_functions import init_db

logger = logging.getLogger(__name__)


async def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(filename)s:%(lineno)d #%(levelname)-8s "
               "[%(asctime)s] - %(name_registrate)s - %(message)s",
    )
    logger.info("Starting bot")
    config: Config = load_config()

    bot: Bot = Bot(token=config.tg_bot.token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    dp: Dispatcher = Dispatcher()

    dp.include_router(stateHandler.form_router)
    # Initialize Bot instance with default bot properties which will be passed to all API calls

    init_db()

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
