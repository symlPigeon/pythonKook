from pyKook.Api.baseApi import baseAPI, multiPageAPI
import logging

from pyKook.Config.config import accountConfig


class getUserGroupListAPI(multiPageAPI):
    """
    获取用户群组接口
    """

    def __init__(self, config: accountConfig):
        super().__init__("/api/v3/guild/list", "get", config)

    def _render(self, data: dict) -> list:
        try:
            items = data["items"]
        except KeyError:
            logging.error("Invalid response!")
            items = ""
        return items


class getGroupInfoAPI(baseAPI):
    """
    获取群组详细信息
    """

    def __init__(self, config: accountConfig, groupid: str):
        super().__init__("/api/v3/guild/view", "get", config, guild_id=groupid)
        self._group_info = {}

    def _render(self, data: dict) -> dict:
        self._group_info = data
        return self._group_info

    def getRoles(self) -> dict:
        """
        获取用户在群组里面的角色
        :return:
        """
        # 如果没有数据就刷新数据
        if self._group_info == {}:
            self._render(self._request())
        try:
            return self._group_info["roles"]
        except KeyError:
            logging.error("No roles found in group info!")
            return {}

    def getChannels(self) -> dict:
        """
        获取群组的频道信息
        :return:
        """
        # 如果没有数据就刷新数据
        if self._group_info == {}:
            self._render(self._request())
        try:
            return self._group_info["channels"]
        except KeyError:
            logging.error("No channels found in group info!")
            return {}

    def getGroupInfo(self) -> dict:
        """
        获取群组的基本信息
        :return:
        """
        if self._group_info == {}:
            self._render(self._request())
        data = self._group_info.copy()
        if "channels" in data:
            del data["channels"]
        if "roles" in data:
            del data["roles"]
        return data
