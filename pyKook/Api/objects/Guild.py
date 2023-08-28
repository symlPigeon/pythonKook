from pyKook.Api.objects.Role import Role
from pyKook.Api.objects.Channel import Channel
import json


class Guild:
    def __init__(self, **kwargs):
        self._id = kwargs.get("id") or ""
        self._name = kwargs.get("name") or ""
        self._topic = kwargs.get("topic") or ""
        self._user_id = kwargs.get("user_id") or ""
        self._icon = kwargs.get("icon") or ""
        self._notify_type = kwargs.get("notify_type") or 0
        self._region = kwargs.get("region") or ""
        self._is_open = kwargs.get("enable_open") or False
        self._open_id = kwargs.get("open_id") or ""
        self._default_chn_id = kwargs.get("default_channel_id") or ""
        self._welcome_chn_id = kwargs.get("welcome_channel_id") or ""
        _roles = kwargs.get("roles") or []
        self._roles = []
        for role in _roles:
            self._roles.append(Role(**role))
        _chns = kwargs.get("channels") or []
        self._channels = []
        for chn in _chns:
            self._channels.append(Channel(**chn))

    def __str__(self):
        return self._id

    def __dict__(self):
        return {
            "id": self._id,
            "name": self._name,
            "topic": self._topic,
            "user_id": self._user_id,
            "icon": self._icon,
            "notify_type": self._notify_type,
            "region": self._region,
            "enable_open": self._is_open,
            "open_id": self._open_id,
            "default_channel_id": self._default_chn_id,
            "welcome_channel_id": self._welcome_chn_id,
            "roles": [json.dumps(role.__dict__()) for role in self._roles],
            "channels": [json.dumps(chn.__dict__()) for chn in self._channels],
        }

    def dump(self):
        return json.dumps(self.__dict__())

    def getId(self) -> str:
        """
        获取群组ID
        :return:
        """
        return self._id

    def getName(self) -> str:
        """
        获取群组名称
        :return:
        """
        return self._name

    def getTopic(self) -> str:
        """
        获取群组主题
        :return:
        """
        return self._topic

    def getUserId(self) -> str:
        """
        获取群组创建者ID
        :return:
        """
        return self._user_id

    def getIcon(self) -> str:
        """
        获取群组头像
        :return:
        """
        return self._icon

    def getNotifyType(self) -> int:
        """
        获取群组通知类型
        :return:
        """
        return self._notify_type

    def getRegion(self) -> str:
        """
        获取语音默认区域
        :return:
        """
        return self._region

    def isOpen(self) -> bool:
        """
        获取是否开启开放群组
        :return:
        """
        return self._is_open

    def getOpenId(self) -> str:
        """
        获取开放群组ID
        :return:
        """
        return self._open_id

    def getDefaultChannelId(self) -> str:
        """
        获取默认频道ID
        :return:
        """
        return self._default_chn_id

    def getWelcomeChannelId(self) -> str:
        """
        获取欢迎频道ID
        :return:
        """
        return self._welcome_chn_id

    def getRoles(self) -> list[Role]:
        """
        获取群组角色列表
        :return:
        """
        return self._roles

    def getChannels(self) -> list[Channel]:
        """
        获取群组频道列表
        :return:
        """
        return self._channels
