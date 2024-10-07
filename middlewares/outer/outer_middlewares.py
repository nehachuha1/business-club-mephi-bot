from aiogram import BaseMiddleware, Bot
from aiogram.types import TelegramObject, User

from typing import Any, Callable, Awaitable, Dict
import logging

from database.postgres import Database
from config.config import load_env

logger = logging.getLogger(__name__)

class MainOuterMiddleware(BaseMiddleware):
    def __init__(self, db: Database) -> None:
        self.db = db
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any], 
        ) -> Any:

        user: User = data['event_from_user']

        data['db'] = self.db
        data['is_registered'] = self.db.check_registration(username=str(user.id))

        return await handler(event, data)