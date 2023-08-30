from pyKook.Api.baseApi import multiPageAPI
from pyKook.Config.accountConfig import accountConfig
from pyKook.Api.objects.User import User
from pyKook.Utils.loggingTool import logging


class getUserInGroupAPI(multiPageAPI):
    def __init__(self, conf: accountConfig, group_id: str, **query_options):
        args = {"guild_id": group_id, **query_options}
        super().__init__("/api/v3/guild/user-list", "get", conf, **args)
        self._user_count = 0
        self._online_user_cnt = 0
        self._offline_user_cnt = 0

    def _render(self, data: dict) -> list:
        try:
            self._user_count = data["user_count"]
            self._online_user_cnt = data["online_count"]
            self._offline_user_cnt = data["offline_count"]
            return data["items"]
        except KeyError as e:
            logging.error("Invalid response! Missing Key: {}".format(e))
            logging.error("Data: {}".format(data))
            self._user_count = 0
            self._online_user_cnt = 0
            self._offline_user_cnt = 0
            return []

    async def getOnlineUserCount(self, update: bool = False) -> int:
        """
        获取当前在线用户数量
        :param update: 是否重新请求而不是使用本地缓存数据
        :return:
        """
        if update or not self._cached_partial_resp and not self._cached_resp:
            await self.getOnePageData()  # 不用全请求，只请求一页就行，省点流量
        return self._online_user_cnt

    async def getOfflineUserCount(self, update: bool = False) -> int:
        """
        获取当前离线用户数量
        :param update: 是否重新请求而不是使用本地缓存数据
        :return:
        """
        if update or not self._cached_partial_resp and not self._cached_resp:
            await self.getOnePageData()
        return self._offline_user_cnt

    async def getUserCount(self, update: bool = False) -> int:
        """
        获取当前群组用户数量
        :param update: 是否重新请求而不是使用本地缓存数据
        :return:
        """
        if update or not self._cached_partial_resp and not self._cached_resp:
            await self.getOnePageData()
        return self._user_count

    async def getUserList(self) -> list:
        """
        获取当前群组用户列表
        :return:
        """
        if not self._cached_resp:
            await self.getData()
        user_list = []
        for user in self._cached_data:
            user_list.append(User(**user))
        return user_list
