from aiogram import executor

from telegram_bot.bot_init import dp
from telegram_bot.handlers import commands


def main():
    commands.register_handlers_commands(dp)
    executor.start_polling(dp, skip_updates=True)


if __name__ == "__main__":
    main()
