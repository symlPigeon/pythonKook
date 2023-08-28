import json


class Role:
    def __init__(self, **kwargs):
        self._role_id = kwargs.get("id") or ""
        self._name = kwargs.get("name") or ""
        self._color = kwargs.get("color") or 0x000000
        self._hoist = kwargs.get("hoist") or 0
        self._position = kwargs.get("position") or 0
        self._mentionable = kwargs.get("mentionable") or 0
        self._permissions = kwargs.get("permissions") or 0

    def __str__(self):
        return self._role_id

    def __dict__(self):
        return {
            "id": self._role_id,
            "name": self._name,
            "color": self._color,
            "hoist": self._hoist,
            "position": self._position,
            "mentionable": self._mentionable,
            "permissions": self._permissions,
        }

    def dump(self):
        return json.dumps(self.__dict__())

    def getId(self) -> str:
        """
        获取角色ID
        :return:
        """
        return self._role_id

    def getName(self) -> str:
        """
        获取角色名称
        :return:
        """
        return self._name

    def getColor(self) -> int:
        """
        获取角色颜色
        :return:
        """
        return self._color

    def isSeperate(self) -> bool:
        """
        获取这个角色设定是否和其他角色分开显示
        :return:
        """
        return self._hoist == 1

    def getPosition(self) -> int:
        """
        获取角色在列表中的位置
        :return:
        """
        return self._position

    def isMentionable(self) -> bool:
        """
        获取角色是否可以被提及
        :return:
        """
        return self._mentionable == 1

    def getPermissions(self) -> int:
        """
        获取角色的权限
        :return:
        """
        return self._permissions
