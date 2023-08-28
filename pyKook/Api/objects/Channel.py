from pyKook.Api.objects.User import User
import json


class Channel:
    def __init__(self, **kwargs):
        self._id = kwargs.get("id") or ""
        self._name = kwargs.get("name") or ""
        self._user_id = kwargs.get("user_id") or ""
        self._guild_id = kwargs.get("guild_id") or ""
        self._topic = kwargs.get("topic") or ""
        self._is_category = kwargs.get("is_category") or False
        self._parent_id = kwargs.get("parent_id") or ""
        self._level = kwargs.get("level") or 0
        self._slow_mode = kwargs.get("slow_mode") or 0
        self._type = kwargs.get("type") or 0
        self._permission_overwrites = kwargs.get("permission_overwrites") or []
        _permission_users = kwargs.get("permission_users") or []
        self._permission_users = []
        for user in _permission_users:
            self._permission_users.append(User(**user))
        self._permission_sync = kwargs.get("permission_sync") or 0
        self._has_password = kwargs.get("has_password") or False

    def __str__(self):
        return self._id

    def __dict__(self):
        return {
            "id": self._id,
            "name": self._name,
            "user_id": self._user_id,
            "guild_id": self._guild_id,
            "topic": self._topic,
            "is_category": self._is_category,
            "parent_id": self._parent_id,
            "level": self._level,
            "slow_mode": self._slow_mode,
            "type": self._type,
            "permission_overwrites": self._permission_overwrites,
            "permission_users": [
                json.dumps(user.__dict__()) for user in self._permission_users
            ],
            "permission_sync": self._permission_sync,
            "has_password": self._has_password,
        }

    def dump(self):
        return json.dumps(self.__dict__())

    def getId(self) -> str:
        """
        获取频道ID
        :return:
        """
        return self._id

    def getName(self) -> str:
        """
        获取频道名称
        :return:
        """
        return self._name

    def getUserId(self) -> str:
        """
        获取创建者ID
        :return:
        """
        return self._user_id

    def getGuildId(self) -> str:
        """
        获取所在服务器ID
        :return:
        """
        return self._guild_id

    def getTopic(self) -> str:
        """
        获取频道主题
        :return:
        """
        return self._topic

    def isCategory(self) -> bool:
        """
        获取是否是分类
        :return:
        """
        return self._is_category

    def getParentId(self) -> str:
        """
        获取所在群组的ID，如果没有则返回空串或者"0"
        :return:
        """
        return self._parent_id

    def getLevel(self) -> int:
        """
        获取频道排序
        :return:
        """
        return self._level

    def getSlowMode(self) -> int:
        """
        获取频道发言限制时间
        :return:
        """
        return self._slow_mode

    def getType(self) -> int:
        """
        获取频道类型，1为文字，2为语音
        :return:
        """
        return self._type

    def getPermissionOverwrites(self) -> list:
        """
        获取频道权限
        :return:
        """
        return self._permission_overwrites

    def getPermissionUsers(self) -> list:
        """
        获取频道权限用户
        :return:
        """
        return self._permission_users

    def isPermissionSync(self) -> bool:
        """
        获取频道权限是否同步
        :return:
        """
        return self._permission_sync
