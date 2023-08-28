from pyKook.Api.objects.User import User
from pyKook.Api.constants.messageType import MSG_TYPE
import json


class Quote:
    def __init__(self, **kwargs):
        self._id = kwargs.get("id") or ""
        self._type = kwargs.get("type") or int(MSG_TYPE.TEXT)
        self._content = kwargs.get("content") or ""
        self._create_at = kwargs.get("create_at") or 0
        self._author = User(**kwargs.get("author")) or User()

    def __str__(self):
        return self._id + "(Quoted)"

    def __dict__(self):
        return {
            "id": self._id,
            "type": self._type,
            "content": self._content,
            "create_at": self._create_at,
            "author": self._author,
        }

    def dump(self):
        return json.dumps(self.__dict__())

    def getId(self) -> str:
        """
        获取引用消息ID
        :return:
        """
        return self._id

    def getType(self) -> int:
        """
        获取引用消息类型
        :return:
        """
        return self._type

    def getContent(self) -> str:
        """
        获取引用消息内容
        :return:
        """
        return self._content

    def getCreateTime(self) -> int:
        """
        获取引用消息发送时间
        :return:
        """
        return self._create_at

    def getAuthor(self) -> User:
        """
        获取引用消息发送者
        :return:
        """
        return self._author
