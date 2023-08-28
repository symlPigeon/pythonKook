from pyKook.Api.baseApi import baseAPI, multiPageAPI
from pyKook.Api.objects.Channel import Channel
from pyKook.Config.config import accountConfig


class getChannelListAPI(multiPageAPI):
    def __init__(self, config: accountConfig, guild_id: str):
        super().__init__("/api/v3/channel/list", "get", config, guild_id=guild_id)

    def _render(self, data: dict) -> list:
        return data["items"]

    async def getChannelIdList(self) -> list[str]:
        """
        获取频道ID列表
        :return:
        """
        channels = await self.getCached()
        id_list = []
        for channel in channels:
            id_list.append(channel["id"])
        return id_list

    async def getChannelList(self, update: bool = False) -> list[Channel]:
        """
        获取频道列表
        :: WARNING :: 这部分得到的频道列表缺少Channel类中应有的字段，请注意区分！
        :return:
        """
        if update:
            channels = await self.getData()
        else:
            channels = await self.getCached()
        channel_list = []
        for channel in channels:
            channel_list.append(Channel(**channel))
        return channel_list

    async def getChannelListFull(self) -> list[Channel | None]:
        """
        获取频道列表
        :return:
        """
        channels = await self.getCached()
        channel_list = []
        for channel in channels:
            channel_id = channel["id"]
            channel_list.append(
                await getChannelInfoAPI(self._config, channel_id).getChannel()
            )
        return channel_list


class getChannelInfoAPI(baseAPI):
    def __init__(self, config: accountConfig, channel_id: str):
        super().__init__("/api/v3/channel/view", "get", config, channel_id=channel_id)

    def _render(self, data: dict) -> dict:
        return data

    async def getChannel(self) -> Channel:
        """
        获取频道信息
        :return:
        """
        return Channel(**await self.getData())
