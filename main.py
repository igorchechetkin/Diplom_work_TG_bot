from TG_API.core import BotStart


bot = BotStart()
bot.command_handler("start")
bot.command_handler("low")
bot.command_handler("high")
bot.command_handler("history")
bot.command_handler("help")
bot.command_handler("unknown")


if __name__ == "__main__":

    bot.bot_start()
