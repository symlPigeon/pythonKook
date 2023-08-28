import json


class Attachment:
    def __init__(self, **kwargs):
        self._type = kwargs.get("type") or ""
        self._url = kwargs.get("url") or ""
        self._name = kwargs.get("name") or ""
        self._size = kwargs.get("size") or 0

    def __str__(self):
        return self._url

    def __dict__(self):
        return {
            "type": self._type,
            "url": self._url,
            "name": self._name,
            "size": self._size,
        }

    def dump(self):
        return json.dumps(self.__dict__())

    def getType(self) -> str:
        """
        获取附件类型
        :return:
        """
        return self._type

    def getUrl(self) -> str:
        """
        获取附件链接
        :return:
        """
        return self._url

    def getName(self) -> str:
        """
        获取附件名称
        :return:
        """
        return self._name

    def getSize(self) -> int:
        """
        获取附件大小
        :return:
        """
        return self._size
