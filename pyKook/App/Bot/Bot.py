from pyKook.Api.objects.User import User
from pyKook.App.Object import Message
from pyKook.Api.constants.messageType import MSG_TYPE
from pyKook.App.Session.sessionPool import sessionPool
from pyKook.Api.eventAPI.msgHandler import websocketMsgHandler
from pyKook.Api.gateway.gateway import getGatewayAPI
from pyKook.Api.userInterface.userInfo import getCurrentUserInfoAPI
from pyKook.Api.channelMessageInterface.channelMessage import (
    sendChannelMsgAPI,
    deleteChannelMsgAPI,
)
from pyKook.Utils.cache import CACHED_INFO
from pyKook.Config import accountConfig, botConfig
from functools import wraps
import logging


class Bot:
    def __init__(self, configs):
        logging.info("System initializing...")
        self._accountConfig: accountConfig = configs["accountConfig"]
        self._botConfig: botConfig = configs["botConfig"]
        self._session_pool = sessionPool(self)
        self._wshandler = None
        self._bot_info = User()
        self._callback_pool = {}
        self._cached_info = CACHED_INFO

    async def _msg_handler(self, event_id: str, msg: Message):
        if event_id == "normalMessage":
            if msg.content().startswith(self._botConfig.getCommand()):
                # 指令消息
                event_id = "command." + msg.content()[1:].split(" ")[0]
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

    def on_command(self, command_id: str):
        return self.on_event("command." + command_id)

    async def _preinit_get_gateway(self) -> str:
        logging.info("Fetching gateway...")
        url = await getGatewayAPI(self._accountConfig).getGateway()
        logging.info("Gateway fetched.")
        return url

    async def _get_basic_info(self):
        logging.info("Fetching basic info of bot...")
        self._bot_info = await getCurrentUserInfoAPI(self._accountConfig).getUserInfo()
        self._cached_info.addUser(self._bot_info)
        logging.info("Basic info fetched.")

    async def initialize(self):
        logging.info("Initializing bot...")
        url = await self._preinit_get_gateway()
        await self._get_basic_info()
        if url == "":
            raise Exception("Failed to get gateway.")
        self._wshandler = websocketMsgHandler()
        self._wshandler.init(self._msg_handler, self._bot_info, self._session_pool)
        logging.info("Bot initialized.")
        await self._wshandler.start(url)

    async def sendText(self, channelId: str, content: str, reply: Message = None):
        """
        发送简单文本消息
        :param channelId: 需要发送的频道ID
        :param content: 发送的内容
        :param reply: 回复的消息
        :return:
        """
        if reply is not None:
            await sendChannelMsgAPI(
                self._accountConfig,
                channelId,
                content,
                quote=reply.getId(),
                msg_type=int(MSG_TYPE.TEXT),
            ).send()
        else:
            await sendChannelMsgAPI(
                self._accountConfig, channelId, content, msg_type=int(MSG_TYPE.TEXT)
            ).send()
