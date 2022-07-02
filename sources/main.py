#!/home/digital/telegram_bots/shop-list-telegram-bot/.venv/bin/python


from aiogram import executor
from dotenv import load_dotenv
import logging

load_dotenv()

from telegram_bot.bot_init import dp
from telegram_bot.handlers import commands
from telegram_bot.bot_init import on_startup, on_shutdown
from telegram_bot.config import WEBHOOK_URL, WEBHOOK_PATH, WEBAPP_HOST, WEBAPP_PORT

logging.basicConfig(filename='./bot.log',
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)

logging.info("bot is up")
logger = logging.getLogger('shop-list-bot-logger')


def main():
    commands.register_handlers_commands(dp)
    executor.start_webhook(
                           dispatcher=dp,
                           webhook_path=WEBHOOK_PATH,
                           skip_updates=True,
                           on_startup=on_startup,
                           on_shutdown=on_shutdown,
                           host=WEBAPP_HOST,
                           port=WEBAPP_PORT
    )


if __name__ == "__main__":
    main()
