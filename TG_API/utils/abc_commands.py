import logging

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    filters,
    MessageHandler
)

from common_settings.settings import BotSettings
from database.core import DBFactory
from logger.core import logged

bot_settings = BotSettings()
database_request = DBFactory()


class StartCommand():

    async def start_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_name = update.message.from_user.first_name
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"{user_name}, тебя приветствует бот "
                                                                              f"поиска информации баскетбольной"
                                                                              f" ассоциации NBA!")


class MinimumCommand():

    @logged
    async def minimum_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):

        logging.info("Пользователем выбрана команда сбора данных об игроках")

        retrieved_data = database_request.handle("db_players")
        data = [f"{retrieve.id} {retrieve.first_name} {retrieve.last_name}" for retrieve in retrieved_data]
        update_data = "\n".join(data)

        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text=f"Ты выбрал(a) команду показа 25ти игроков лиги! Наслаждайся:\n"
                                            f" id   Имя   Фамилия\n-------------------------------\n"
                                            f"{update_data}")


class MaximumCommand():
    @logged
    async def maximum_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):

        logging.info("Пользователем выбрана команда сбора данных о командах")

        retrieved_data = database_request.handle("db_teams")
        data = [f"{retrieve.id} {retrieve.conference} {retrieve.full_name}" for retrieve in retrieved_data]
        teams_data = "\n".join(data)

        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text=f"Ты выбрал(a) команду показа 30ти команд лиги! Наслаждайся:\n"
                                            f" id   Конференция  Команда\n-------------------------------\n"
                                            f"{teams_data}")


class HistoryCommand():
    @logged
    async def history_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):

        logging.info("Пользователем выбрана команда просмотра истории запросов")

        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text="Здесь будет история запросов")

class HelpCommand():
    @logged
    async def help_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):

        logging.info("Пользователем выбрана команда просмотра истории запросов")

        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text=f"Я умею выполнять следующие команды:\n"
                                            f"/start    - запускаем бота\n"
                                            f"/low      - минимум\n"
                                            f"/high     - максимум\n"
                                            f"/history  - история запросов\n"
                                            f"/help     - помощь")


class UnknownCommand():

    @logged
    async def unknown_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):

        logging.info("Пользователь ввел неизвестную команду")

        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text="Введите корректную команду! Они указаны в кнопке меню "
                                            "или воспользуйтесь командой /help")


class BotStart():

    token = bot_settings.token.get_secret_value()
    application = ApplicationBuilder().token(token).build()

    def bot_start(self):
        start_handler = CommandHandler("start", StartCommand.start_callback)
        low_handler = CommandHandler("low", MinimumCommand.minimum_callback)
        high_handler = CommandHandler("high", MaximumCommand.maximum_callback)
        history_handler = CommandHandler("history", HistoryCommand.history_callback)
        help_handler = CommandHandler("help", HelpCommand.help_callback)
        unknown_handler = MessageHandler(filters.COMMAND, UnknownCommand.unknown_callback)

        self.application.add_handler(start_handler)
        self.application.add_handler(low_handler)
        self.application.add_handler(high_handler)
        self.application.add_handler(history_handler)
        self.application.add_handler(help_handler)
        self.application.add_handler(unknown_handler)
        self.application.run_polling()


if __name__ == "__main__":

    BotStart()
