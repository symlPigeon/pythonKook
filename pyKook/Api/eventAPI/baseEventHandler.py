from pyKook.Api.eventAPI.msgHandler import websocketMsgHandler
from pyKook.Utils.singleton import singleton
from typing import Tuple


@singleton
class baseEventHandler:
    def __init__(self):
        self._event = ""

    def register(self):
        # 注册事件
        websocketMsgHandler().register(self._event, self.handle)

    def handle(self, msg: dict) -> Tuple[str, dict]:
        # 对信息extra字段进行处理，返回处理后的信息
        raise NotImplementedError
