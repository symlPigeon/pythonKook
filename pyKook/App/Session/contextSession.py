from pyKook.App.Object import Message
from pyKook.Config.config import accountConfig
from pyKook.Utils.cache import CACHED_INFO
from pyKook.App.Session.sessionPool import sessionPool
from pyKook.Utils.timer import Timer


class contextSession:
    def __init__(
        self,
        channel_id: str,
        condition: callable,
        reaction: callable,
        conf: accountConfig,
        pool: sessionPool,
        timeout: float = 60,
    ):
        self._channel_id = channel_id
        self._condition = condition
        self._reaction = reaction
        self._conf = conf
        self._sessionPool = pool
        self._sessionPool.register(self)
        self._timer = Timer(timeout, self._sessionPool.kill, session=self)

    def _precheck(self, msg: Message) -> bool:
        if self._channel_id != msg.getChannel():
            return False
        return True

    def _check(self, msg: Message) -> bool:
        if not self._precheck(msg):
            return False
        return self._condition(msg)

    async def handle(self, msg: Message) -> bool:
        if not self._check(msg):
            return False
        ans = await self._reaction(msg)
        self._timer.refresh()
        if ans:
            self._sessionPool.kill(self)
        return True
