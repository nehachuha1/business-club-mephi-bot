from dataclasses import dataclass
from dotenv import dotenv_values
import logging

logger = logging.getLogger(__name__)

@dataclass
class TGBot:
    token: str

@dataclass
class Config:
    TGBot: TGBot

def load_env(path: str | None = None):
    env_values = dotenv_values(path)
    return Config(TGBot=TGBot(token=env_values["TOKEN"]))
