import logging
from typing import Tuple
from pyKook.Api.constants.messageType import MSG_TYPE


class Message:
    def __init__(self, msg: dict, event_id: str, callbacks=None):
        self._msg = msg
        self._event_id = event_id
        self._callbacks = {}
        if callbacks:
            self._callbacks = callbacks

    def getGroup(self) -> str:
        """
        获取消息所在的群组
        :return:
        """
        if self._msg["channel_type"] == 255 and self._msg["type"] == MSG_TYPE.SYSTEM:
            return self._msg["target_id"]
        elif self._msg["type"] != MSG_TYPE.SYSTEM:
            return self._msg["extra"]["guild_id"]
        else:
            return ""

    def getChannel(self) -> str:
        """
        获取消息所在的频道
        :return:
        """
        if self._msg["type"] != MSG_TYPE.SYSTEM:
            return self._msg["target_id"]
        return self._msg.get("channel_id", "")

    def getAuthorId(self) -> str:
        """
        获取消息来源
        :return:
        """
        return self._msg["author_id"]

    def content(self) -> str:
        """
        获取消息内容
        :return:
        """
        return self._msg["content"]

    def getId(self) -> str:
        """
        获取消息ID
        :return:
        """
        return self._msg["msg_id"]

    def getCallback(self, value: str) -> tuple[callable, dict]:
        """
        获取这个消息绑定事件的回调函数，如果有的话……
        :param value:
        :return:
        """
        if value in self._callbacks:
            return self._callbacks[value]
        return None, {}
