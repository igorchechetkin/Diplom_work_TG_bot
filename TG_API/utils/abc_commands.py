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
players_data = DBFactory()
# teams_response = RequestsInterface.teams_request()


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

        retrieved_data = players_data.handle("db_players")
        data = [f"{retrieve.id} {retrieve.first_name} {retrieve.last_name}" for retrieve in retrieved_data]
        update_data = "\n".join(data)
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text=f"Ты выбрал(a) команду показа 25ти игроков лиги! Наслаждайся:\n"
                                            f" id   Имя   Фамилия\n-------------------------------\n"
                                            f"{update_data}")

#
# class MaximumCommand():
#
#     async def maximum_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
#
#         teams_data = "\n".join(teams_response)
#
#         await context.bot.send_message(chat_id=update.effective_chat.id,
#                                        text=f"Ты выбрал(a) команду показа 30ти команд лиги! Наслаждайся:\n"
#                                             f" id   Конференция  Команда\n-------------------------------\n"
#                                             f"{teams_data}")


class BotStart():

    token = bot_settings.token.get_secret_value()
    application = ApplicationBuilder().token(token).build()

    def bot_start(self):
        start_handler = CommandHandler("start", StartCommand.start_callback)
        low_handler = CommandHandler("low", MinimumCommand.minimum_callback)
        # high_handler = CommandHandler("high", MaximumCommand.maximum_callback)

        self.application.add_handler(start_handler)
        self.application.add_handler(low_handler)
        # self.application.add_handler(high_handler)
        self.application.run_polling()


if __name__ == "__main__":

    BotStart()
