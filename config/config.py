from dataclasses import dataclass
from typing import List

from dotenv import load_dotenv

from .base import getenv, ImproperlyConfigured


@dataclass
class TelegramBotConfig:
    token: str


@dataclass
class Config:
    tg_bot: TelegramBotConfig

def load_config() -> Config:
    # Parse a `.env` file and load the variables into environment valriables
    load_dotenv()

    return Config(tg_bot=TelegramBotConfig(
        token=getenv("TELEGRAM_TOKEN"),
    ))

@dataclass
class PayYoomoney:
    SUCCES_TOKEN_YOOMONEY: str
    PRICE_AMOUNT: int
    RECEIVER_YOOMONEY: str

def load_price() -> PayYoomoney:

    load_dotenv()

    return PayYoomoney(
        SUCCES_TOKEN_YOOMONEY=getenv("SUCCES_TOKEN_YOOMONEY"),
        PRICE_AMOUNT=int(getenv("PRICE_AMOUNT")),
        RECEIVER_YOOMONEY=getenv("RECEIVER_YOOMONEY"),
    )