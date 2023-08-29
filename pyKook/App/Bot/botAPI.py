from .Bot import Bot
from ..Object import Message, Card


class botAPI(Bot):
    """
    这个类仅仅是用来给插件系统提供API提示和补全的，实际上屁用没有
    """

    def __init__(self, configs):
        pass

    def on_setup(self):
        pass

    def on_startup(self):
        pass

    def on_command(self, command_id: str):
        pass

    def on_event(self, event_id: str, privileged: bool = False):
        pass

    def privileged(self, command_id: str):
        pass

    def initialize(self):
        pass

    def getAllMessages(self):
        pass

    def getMessageById(self, msg_id: str):
        pass

    async def sendText(
        self, channelId: str, content: str, reply: Message = None
    ) -> str:
        pass

    async def sendRichText(
        self, channelId: str, content: str, reply: Message = None
    ) -> str:
        pass

    async def sendCardText(self, channelId: str, content: Card) -> str:
        pass

    async def deleteMessage(self, message: Message):
        pass
