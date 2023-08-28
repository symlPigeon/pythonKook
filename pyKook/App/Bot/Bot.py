from pyKook.Api.objects.User import User
from pyKook.App.Object import Message
from pyKook.App.Session.sessionPool import sessionPool
from pyKook.Api.eventAPI.msgHandler import websocketMsgHandler
from pyKook.Api.gateway.gateway import getGatewayAPI
from pyKook.Api.userInterface.userInfo import getCurrentUserInfoAPI
from functools import wraps
import logging


class Bot:
    def __init__(self, configs):
        logging.info("System initializing...")
        self._accountConfig = configs["accountConfig"]
        self._botConfig = configs["botConfig"]
        self._session_pool = sessionPool(self)
        self._wshandler = None
        self._bot_info = User()
        self._callback_pool = {}

    async def _msg_handler(self, event_id: str, msg: Message):
        if event_id in self._callback_pool:
            logging.info("Processing event: %s" % event_id)
            await self._callback_pool[event_id](msg)
        else:
            logging.warning("Event not handled: %s" % event_id)

    def on_event(self, event_id: str):
        def _wrap_on_event(callback):
            self._callback_pool[event_id] = callback
            logging.info(
                "Warping function {} for event id {}".format(callback, event_id)
            )

            @wraps(callback)
            def _warp():
                return callback

            return _warp

        return _wrap_on_event

    async def initialize(self):
        logging.info("Initializing bot...")
        url = await getGatewayAPI(self._accountConfig).getGateway()
        self._bot_info = await getCurrentUserInfoAPI(self._accountConfig).getUserInfo()
        if url == "":
            raise Exception("Failed to get gateway.")
        self._wshandler = websocketMsgHandler()
        self._wshandler.init(self._msg_handler, self._bot_info, self._session_pool)
        logging.info("Bot initialized.")
        await self._wshandler.start(url)
