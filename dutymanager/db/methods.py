from module.utils.context import ContextInstanceMixin
from tortoise import Tortoise
from .standard import *


class AsyncDatabase(ContextInstanceMixin):
    def __init__(self):
        self.chats = Chats()
        self.trusted = Proxies()
        self.templates = Templates()

    async def init(self):
        await Tortoise.init(
            db_url="sqlite://dutymanager/core/duty.db",
            modules={"models": ["dutymanager.db.models"]}
        )
        await Tortoise.generate_schemas()
        await self.load_values()

    async def load_values(self):
        async for i in Chat.all():
            self.chats[i.uid] = {
                "id": i.id, "title": i.title
            }

        async for x in Trusted.all():
            self.trusted[x.id] = x.name

        async for y in Template.all():
            self.templates[y.tag] = {
                "message": y.text,
                "attachment": y.attachments
            }


db = AsyncDatabase()
AsyncDatabase.set_current(db)