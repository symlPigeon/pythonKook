from pyKook.Api.baseApi import baseAPI, multiPageAPI
from pyKook.Utils.loggingTool import logging

from pyKook.Config.accountConfig import accountConfig
from pyKook.Api.objects.Guild import Guild
from pyKook.Api.objects.Role import Role
from pyKook.Api.objects.Channel import Channel


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
            items = []
        return items

    async def getGroupIdList(self) -> list[str]:
        """
        获取群组列表
        :return:
        """
        groups = await self.getCached()
        id_list = []
        for group in groups:
            id_list.append(group["id"])
        return id_list


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

    async def getRoles(self) -> list[Role]:
        """
        获取用户在群组里面的角色
        :return:
        """
        # 如果没有数据就刷新数据
        if self._group_info == {}:
            self._render(await self._request())
        try:
            roles = []
            for role in self._group_info["roles"]:
                roles.append(Role(**role))
            return roles
        except KeyError:
            logging.error("No roles found in group info!")
            return []

    async def getChannels(self) -> list[Channel]:
        """
        获取群组的频道信息
        :return:
        """
        # 如果没有数据就刷新数据
        if self._group_info == {}:
            self._render(await self._request())
        try:
            chns = []
            for chn in self._group_info["channels"]:
                chns.append(Channel(**chn))
            return chns
        except KeyError:
            logging.error("No channels found in group info!")
            return []

    async def getGroupInfo(self) -> Guild:
        """
        获取群组的基本信息
        :return:
        """
        if self._group_info == {}:
            self._render(await self._request())
        return Guild(**self._group_info)
