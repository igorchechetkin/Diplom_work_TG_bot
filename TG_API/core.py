from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    filters,
    MessageHandler
)

from common_settings.settings import BotSettings
from TG_API.utils.abc_commands import CommandFactory


bot_settings = BotSettings()
command_made = CommandFactory()


class BotStart():

    token = bot_settings.token.get_secret_value()
    application = ApplicationBuilder().token(token).build()

    COMMANDS = {
        "start": command_made.handle("start"),
        "low": command_made.handle("minimum"),
        "high": command_made.handle("maximum"),
        "history": command_made.handle("history"),
        "help": command_made.handle("help"),
    }

    MESSAGE = {
        "unknown": command_made.handle("unknown")
    }

    def command_handler(self, command: str):

        if command in self.COMMANDS.keys():
            command_calling = self.COMMANDS.get(command).callback
            handler = CommandHandler(command, command_calling)

        else:
            command_calling = self.MESSAGE.get(command).callback
            handler = MessageHandler(filters.COMMAND, command_calling)

        self.application.add_handler(handler)

    def bot_start(self) -> None:

        self.application.run_polling()


if __name__ == "__main__":

    BotStart()
