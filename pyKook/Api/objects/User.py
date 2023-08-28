import json


class User:
    def __init__(self, **kwargs):
        self._id = kwargs.get("id") or ""
        self._name = kwargs.get("username") or ""
        self._nickname = kwargs.get("nickname") or ""
        self._identify_num = kwargs.get("identify_num") or ""
        self._is_online = kwargs.get("online") or False
        self._is_bot = kwargs.get("bot") or False
        self._avatar = kwargs.get("avatar") or ""
        self._vip_avatar = kwargs.get("vip_avatar") or ""
        self._is_mobile_verified = kwargs.get("mobile_verified") or False
        self._roles = kwargs.get("roles") or []

    def __dict__(self):
        return {
            "id": self._id,
            "username": self._name,
            "nickname": self._nickname,
            "identify_num": self._identify_num,
            "online": self._is_online,
            "bot": self._is_bot,
            "avatar": self._avatar,
            "vip_avatar": self._vip_avatar,
            "mobile_verified": self._is_mobile_verified,
            "roles": self._roles,
        }

    def __str__(self):
        return self._name

    def dump(self):
        return json.dumps(self.__dict__())

    def getId(self) -> str:
        """
        获取用户ID
        :return:
        """
        return self._id

    def getName(self) -> str:
        """
        获取用户名
        :return:
        """
        return self._name

    def getNickName(self) -> str:
        """
        获取用户昵称
        :return:
        """
        return self._nickname

    def getIdentifyNum(self) -> str:
        """
        获取用户认证数字（用户名井号后面的依托东西）
        :return:
        """
        return self._identify_num

    def isOnline(self) -> bool:
        """
        获取用户在线状态
        :return:
        """
        return self._is_online

    def isBot(self) -> bool:
        """
        获取用户是否为机器人
        :return:
        """
        return self._is_bot

    def getAvatarUrl(self) -> str:
        """
        获取用户头像URL
        :return:
        """
        return self._avatar

    def getVipAvatarUrl(self) -> str:
        """
        获取用户VIP头像URL
        :return:
        """
        return self._vip_avatar

    def isMobileVerified(self) -> bool:
        """
        获取用户是否已经绑定手机
        :return:
        """
        return self._is_mobile_verified

    def getRole(self) -> list:
        """
        获取用户的角色列表
        :return:
        """
        return self._roles
