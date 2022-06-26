from aiogram import executor

from telegram_bot.bot_init import dp
from telegram_bot.handlers import commands
from telegram_bot.bot_init import on_startup, on_shutdown
from telegram_bot.config import WEBHOOK_URL, WEBAPP_HOST, WEBAPP_PORT


def main():
    commands.register_handlers_commands(dp)
    executor.start_webhook(
                           dispatcher=dp,
                           webhook_path=WEBHOOK_URL,
                           skip_updates=True,
                           on_startup=on_startup,
                           on_shutdown=on_shutdown,
                           host=WEBAPP_HOST,
                           port=WEBAPP_PORT
    )


if __name__ == "__main__":
    main()
