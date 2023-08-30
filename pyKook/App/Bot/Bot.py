from pyKook.Api.objects.User import User
from pyKook.App.Object import Message, Card
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
from pyKook.Utils.pluginManager import pluginManager
from pyKook.Config import accountConfig, botConfig
from functools import wraps
from pyKook.Utils.loggingTool import logging


class Bot:
    def __init__(self, configs):
        logging.info("System initializing...")
        self._accountConfig: accountConfig = configs["accountConfig"]
        self._botConfig: botConfig = configs["botConfig"]
        self._pluginMgr = pluginManager(self, self._botConfig)
        self._session_pool = sessionPool(self)
        self._wshandler = None
        self._bot_info = User()
        self._callback_pool = {}
        self._privilege_callback_pool = {}
        self._cached_info = CACHED_INFO
        self._startup_list = []

    async def _msg_handler(self, event_id: str, msg: Message):
        # 缓存一下捏
        # self._cached_info.addMessage(msg) # BUG:

        # 处理特殊的消息类型
        match event_id.split(".")[0]:
            case "normalMessage":
                if msg.content().startswith(self._botConfig.getCommand()):
                    logging.info("Command message received: ".format(event_id))
                    # 指令消息
                    event_id = "command." + msg.content()[1:].split(" ")[0]
            case "cardClicked":
                logging.info("Card button clicked: {}".format(event_id))
                # 卡片消息上面的按钮被点击
                card_id = event_id.split(".")[1]
                button_value = event_id.split(".")[2].strip()
                card = self._cached_info.getMessage(card_id)
                if card is None:
                    logging.warning("Card not found! Destroy it!")
                    await self.deleteMessage(Message({"msg_id": card_id}, ""))
                    return
                cb_, args = card.getCallback(button_value)
                if cb_:
                    await cb_(msg, **args)
                return
        if (
            event_id in self._privilege_callback_pool
            and msg.getAuthorId() in self._botConfig.getSuperUsers()
        ):
            logging.info("Processing privileged event: %s" % event_id)
            await self._privilege_callback_pool[event_id](msg)
        if event_id in self._callback_pool:
            logging.info("Processing event: %s" % event_id)
            await self._callback_pool[event_id](msg)
        else:
            logging.warning("Event not handled: %s" % event_id)

    def unload_handler(self, event_id: str, func: callable = None):
        """
        卸载某个事件的处理函数
        :param event_id: 事件ID
        :param func: 可选的，避免两个模组注册同一个事件时出现问题，不过好像不会出现这种情况？？？
        :return:
        """
        if not func:
            logging.info("Unloading event handler: {}".format(event_id))
        else:
            logging.info("Unloading function {} for event {}".format(func, event_id))
        if event_id in self._callback_pool:
            if func.__name__ == self._callback_pool[event_id].__name__ or not func:
                del self._callback_pool[event_id]
                logging.info("Event handler unloaded.")
        # 暂时考虑特权命令不卸载
        # if event_id in self._privilege_callback_pool:
        #     if (
        #         func.__name__ == self._privilege_callback_pool[event_id].__name__
        #         or not func
        #     ):
        #         del self._privilege_callback_pool[event_id]
        #         logging.info("Privilege event handler unloaded.")

    def load_handler(self, event_id: str, func: callable, privileged: bool = False):
        """
        加载某个事件的处理函数
        :param event_id: 事件ID
        :param func: 处理函数
        :return:
        """
        logging.info("Loading function {} for event {}".format(func, event_id))
        if privileged:
            # 这个还是就给一些比较系统级别的东西来用
            self._privilege_callback_pool[event_id] = func
            return
        if event_id in self._callback_pool:
            logging.warning("Event handler already exists! Overwriting...")
        self._callback_pool[event_id] = func

    def on_setup(self):
        def _wrap_on_setup(callback):
            self._startup_list.append(callback)
            logging.info("Warping function {} for startup".format(callback))
            _g = callback.__globals__
            _g["bot"] = self

            @wraps(callback)
            def _warp():
                return callback

            return _warp

        return _wrap_on_setup

    def on_event(self, event_id: str, privileged: bool = False):
        """
        比`on_event`和`privileged`更加基本的修饰器，在各类事件被触发时调用对应的函数。
        请阅读文档（咕咕咕）来了解相应的事件ID。
        :param event_id: 事件ID
        :param privileged: 是否为高权限事件，也就是只有在`botConfig`中的管理员用户才能触发
        :return:
        """

        def _wrap_on_event(callback):
            if privileged:
                self._privilege_callback_pool[event_id] = callback
            else:
                self._callback_pool[event_id] = callback
            # 修改函数__name__便于插件加载器识别
            callback.__name__ = (
                "decorated_on_event@" + event_id + "@" + callback.__name__
            )
            _g = callback.__globals__
            _g["bot"] = self
            logging.info(
                "Warping function {} for event id {}".format(callback, event_id)
            )

            @wraps(callback)
            def _warp():
                return callback

            return _warp

        return _wrap_on_event

    def on_command(self, command_id: str):
        """
        用于注册指令
        :param command_id:
        :return:
        """
        return self.on_event("command." + command_id)

    def privileged(self, command_id: str):
        """
        仅限高权限的命令
        :return:
        """
        return self.on_event("command." + command_id, privileged=True)

    async def _preinit_get_gateway(self) -> str:
        logging.info("Fetching gateway...")
        url = await getGatewayAPI(self._accountConfig).getGateway()
        logging.info("Gateway fetched.")
        return url

    async def _preinit_get_basic_info(self):
        logging.info("Fetching basic info of bot...")
        self._bot_info = await getCurrentUserInfoAPI(self._accountConfig).getUserInfo()
        self._cached_info.addUser(self._bot_info)
        logging.info("Basic info fetched.")

    async def _preinit_run_all_startup_tasks(self):
        logging.info("Running all startup tasks...")
        for task in self._startup_list:
            await task()
        logging.info("All startup tasks finished.")

    def _preinit_load_plugins(self):
        if self._pluginMgr.isEnabled():
            self._pluginMgr.load()

    async def initialize(self):
        logging.info("Initializing bot...")
        url = await self._preinit_get_gateway()
        await self._preinit_get_basic_info()
        await self._preinit_run_all_startup_tasks()
        self._preinit_load_plugins()
        if url == "":
            raise Exception("Failed to get gateway.")
        self._wshandler = websocketMsgHandler()
        self._wshandler.init(self._msg_handler, self._bot_info, self._session_pool)
        logging.info("Bot initialized.")
        await self._wshandler.start(url)

    def _cache_sent_message(
        self,
        content: str,
        msg_id: str,
        channel_id: str,
        callbacks=None,
    ):
        logging.info("Caching sent message...")
        logging.info("Callbacks: {}".format(callbacks))
        self._cached_info.addMessage(
            Message(
                msg={
                    "content": content,
                    "msg_id": msg_id,
                    "target_id": channel_id,
                    "author_id": self._bot_info.getId(),
                },
                event_id="messageSent",
                callbacks=callbacks,
            )
        )

    def getMessageById(self, msg_id: str):
        return self._cached_info.getMessage(msg_id)

    def getAllMessages(self):
        return self._cached_info.getAllMessages()

    async def sendText(
        self, channelId: str, content: str, reply: Message = None
    ) -> str:
        """
        发送简单文本消息
        :param channelId: 需要发送的频道ID
        :param content: 发送的内容
        :param reply: 回复的消息
        :return:
        """
        api = sendChannelMsgAPI(self._accountConfig, channelId, content)
        if reply is not None:
            api.addArgs(quote=reply.getId())
        try:
            msg_id = (await api.send())["msg_id"]
        except KeyError:
            logging.error("Failed to send text!")
            logging.error("Content: {}".format(content))
            return ""
        self._cache_sent_message(content, msg_id, channelId)
        return msg_id

    async def sendRichText(self, channelId: str, content: str, reply: Message = None):
        """
        发送富文本消息
        :param channelId: 需要发送的频道ID
        :param content: 发送的内容
        :param reply: 回复的消息
        :return:
        """
        api = sendChannelMsgAPI(
            self._accountConfig,
            channelId,
            content,
            msg_type=int(MSG_TYPE.KMARKDOWN),
        )
        if reply is not None:
            api.addArgs(quote=reply.getId())
        try:
            msg_id = (await api.send())["msg_id"]
        except KeyError:
            logging.error("Failed to send rich text!")
            logging.error("Content: {}".format(content))
            return
        self._cache_sent_message(content, msg_id, channelId)
        return msg_id

    async def sendCardText(self, channelId: str, content: Card):
        """
        发送卡片消息
        :param channelId: 需要发送的频道ID
        :param content: 卡片信息
        :return:
        """
        card_json = str(content)
        api = sendChannelMsgAPI(
            self._accountConfig,
            channelId,
            card_json,
            msg_type=int(MSG_TYPE.CARD),
        )
        try:
            msg_id = (await api.send())["msg_id"]
        except KeyError:
            logging.error("Failed to send card!")
            logging.error("Card json: {}".format(card_json))
            return
        logging.info("sendCardText ID: {}".format(msg_id))
        print(content.getCallbacks())
        self._cache_sent_message(
            card_json, msg_id, channelId, callbacks=content.getCallbacks()
        )
        return msg_id

    async def deleteMessage(self, message: Message) -> None:
        """
        删除某条消息
        :param message: 需要删除的消息对象
        :return:
        """
        api = deleteChannelMsgAPI(self._accountConfig, message.getId())
        await api.delete()
        self._cached_info.removeMessage(message.getId())
