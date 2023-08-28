from pyKook.App.Object import Message
from pyKook.App.Session import contextSession
from pyKook.App.Bot import Bot


class sessionPool:
    def __init__(self, bot: Bot):
        self._bot = bot
        self._session_pool = {}

    def register(self, session: contextSession):
        if id(session) in self._session_pool:
            return
        self._session_pool[id(session)] = session

    def kill(self, session: contextSession):
        if id(session) not in self._session_pool:
            return
        del self._session_pool[id(session)]

    def handle(self, msg: Message) -> bool:
        for session in self._session_pool.values():
            if session.handle(msg):
                return True
        return False
