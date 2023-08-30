from typing import Callable, Optional

from pyKook.Api.constants.messageType import MSG_TYPE
from pyKook.Api.eventAPI.baseEventHandler import baseEventHandler
from pyKook.Api.objects import User
from pyKook.App.Object import Message
from pyKook.App.Session import sessionPool
from pyKook.Utils.singleton import singleton
from pyKook.Utils.websocketHandler import websocketHandler
from pyKook.Utils.loggingTool import logging


@singleton
class websocketMsgHandler:
    def __init__(self):
        self._event_handlers = {}
        self._ws = None
        self._bot_info = User()
        self._context = None

        # 自动注册模块内定义好的EventHandler
        import inspect
        import pyKook.Api.eventAPI.eventHandler as eventHandler

        print(inspect.getmembers(eventHandler, inspect.isclass))

        for name, obj in inspect.getmembers(eventHandler, inspect.isclass):
            if issubclass(obj, baseEventHandler):
                logging.info("Registering event handler: %s" % name)
                obj().register(self)

        # App模块给过来的函数处理
        async def _nothing_handler(x, y):
            ...

        self._app_handler = _nothing_handler

    def init(self, app_handler, botInfo: User, context: sessionPool):
        self._app_handler = app_handler
        self._bot_info = botInfo
        self._context = context

    def register(self, event: str, handler: Callable[[dict, Optional[User]], str]):
        self._event_handlers[event] = handler

    async def start(self, url: str):
        self._ws = websocketHandler(url, self._msg_handler)
        await self._ws.runHandler()

    async def _msg_handler(self, msg: dict):
        # 如果没太大毛病的话，这里传进来的应该是个str
        logging.info("Processing message received...")
        logging.info("Message: {}".format(msg))
        try:
            # 确保这个消息是按照预期的格式来的
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
                logging.info("Message type: {}".format(msg_type))
                logging.info("sending to text_message handler")
                msg, event_id = self._event_handlers["text_message"](
                    msg, self._bot_info
                )
                message = Message(msg, event_id)
                logging.info("Message event id: {}".format(event_id))
                if self._context.handle(message):
                    logging.info("Message consumed by contextSession!")
                    return  # 很不幸，这条消息被contextSession干掉了
                logging.info("Passing message to app handler...")
                await self._app_handler(event_id, message)
                return
            case MSG_TYPE.SYSTEM:
                # 系统消息，比较麻烦
                try:
                    msg, event_id = self._event_handlers[extra["type"]](
                        msg, self._bot_info
                    )
                except KeyError as e:
                    logging.warning("System message not implemented yet.")
                    return
                message = Message(msg, event_id)
                logging.info("Message event id: {}".format(event_id))
                logging.info("Passing message to app handler...")
                await self._app_handler(event_id, message)
                return
            case _:
                # 不知道啥东西
                logging.error("Unknown message type: {}!".format(msg_type))
                return
