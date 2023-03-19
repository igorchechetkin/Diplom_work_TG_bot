import os

from dotenv import load_dotenv
from pydantic import BaseSettings, SecretStr, StrictInt, StrictStr

load_dotenv()


class SiteSettings(BaseSettings):
    api_key: SecretStr = os.getenv("API_KEY", None)
    api_host: StrictStr = os.getenv("API_HOST", None)
    api_timeout: StrictInt = os.getenv("API_TIMEOUT", 10)


class BotSettings(BaseSettings):
    token: SecretStr = os.getenv("BOT_TOKEN", None)


class ApiFields(BaseSettings):
    fields_players: StrictStr = os.getenv("FIELDS_PLAYERS", None)
    fields_teams: StrictStr = os.getenv("FIELDS_TEAMS", None)
