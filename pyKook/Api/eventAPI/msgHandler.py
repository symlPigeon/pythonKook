from typing import Callable, Tuple

from pyKook.Utils.websocketHandler import websocketHandler
from pyKook.Api.eventAPI.baseEventHandler import baseEventHandler
from pyKook.Utils.singleton import singleton
import logging
from pyKook.Api.constants.messageType import MSG_TYPE


@singleton
class websocketMsgHandler:
    def __init__(self, app_handler: Callable[[str, dict], None]):
        self._event_handlers = {}
        self._ws_pool = {}

        # 自动注册模块内定义好的EventHandler
        import inspect
        import sys

        for name, obj in inspect.getmembers(
            sys.modules["_eventHandler"], inspect.isclass
        ):
            if issubclass(obj, baseEventHandler):
                logging.info("Registering event handler: %s" % name)
                obj().register()

        # App模块给过来的函数处理
        self._app_handler = app_handler

    def register(self, event: str, handler: Callable[[dict], Tuple[str, dict]]):
        self._event_handlers[event] = handler

    def _msg_handler(self, msg: dict):
        # 如果没太大毛病的话，这里传进来的应该是个str
        logging.debug("Processing message received...")
        logging.debug("Message: {}".format(msg))
        try:
            channel_type = str(msg["channel_type"])  # 消息通道类型
            msg_type = int(msg["type"])  # 消息类型
            target_id = str(msg["target_id"])  # 目标ID
            author = str(msg["author_id"])  # 来源，1为系统消息
            content = str(msg["content"])  # 内容
            msg_id = str(msg["msg_id"])  # 消息ID
            msg_timestamp = int(msg["msg_timestamp"])  # 消息时间戳
            nonce = str(msg["nonce"])  # 随机数
            extra = msg["extra"]  # 额外信息
        except KeyError as e:
            # 似乎消息有点问题，那就不处理了，但这值得吗？
            logging.error("Encountered KeyError while processing message!")
            logging.error("Missing Key! {}".format(str(e)))
            logging.error("Message: {}".format(msg))
            return
        match msg_type:
            case MSG_TYPE.TEXT | MSG_TYPE.KMARKDOWN | MSG_TYPE.CARD | MSG_TYPE.AUDIO | MSG_TYPE.FILE | MSG_TYPE.IMAGE | MSG_TYPE.VIDEO:
                # 一般频道消息
                ...
            case MSG_TYPE.SYSTEM:
                # 系统消息，比较麻烦
                ...
            case _:
                # 不知道啥东西
                logging.error("Unknown message type: {}!".format(msg_type))
                return
