from pyKook.Api.objects import User
from typing import Optional, Tuple


class baseEventHandler:
    def __init__(self):
        self._event = ""

    def register(self, ws_handler):
        # 注册事件

        ws_handler.register(self._event, self.handle)

    def handle(self, msg: dict, bot_info: Optional[User]) -> Tuple[dict, str]:
        # 对信息extra字段进行处理，返回处理后的信息
        raise NotImplementedError
