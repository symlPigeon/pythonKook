from pyKook.Config.config import accountConfig
from pyKook.Api.gateway.gateway import getGatewayAPI
from pyKook.Utils.websocketHandler import websocketHandler
from pyKook.Api.serverInterface.serverInfo import getGroupInfoAPI, getUserGroupListAPI
from pyKook.Api.serverInterface.userList import getUserInGroupAPI
from pyKook.Api.channelMessageInterface.channelMessage import (
    sendChannelMsgAPI,
    deleteChannelMsgAPI,
)
from pyKook.Utils.httpHandler import httpHandler
from pyKook.Api.gameStatus.gameList import getGameListAPI
from pyKook.Api.channelInterface.channelList import getChannelListAPI, getChannelInfoAPI

from IGNORE_ME import token  # private information
import asyncio
import logging


async def main():
    conf = accountConfig("Bot", token, "zh-CN")

    userGroupAPI = getUserGroupListAPI(conf)
    groupList = await userGroupAPI.getGroupIdList()

    groupId = groupList[0]
    channelListAPI = getChannelListAPI(conf, groupId)
    channelList = await channelListAPI.getChannelList()
    print(channelList)

    channelListFull = await channelListAPI.getChannelListFull()
    for channel in channelListFull:
        print(channel.getName())

    #
    # groupInfoAPI = getGroupInfoAPI(conf, groupList[0])
    # channels = await groupInfoAPI.getChannels()
    #
    # userAPI = getUserInGroupAPI(conf, groupList[0], active_time=1)
    # users = await userAPI.getData()
    # print(users)

    # target_channel = None
    # for channel in channels:
    #     if channel.getType() == 1:
    #         print(channel.getId())
    #         target_channel = channel.getId()
    #         break
    # message = await sendChannelMsgAPI(conf, target_channel, "测试消息，将在5秒后销毁。").send()
    # print(message)
    # msg_id = message["msg_id"]
    # await asyncio.sleep(5)
    # await deleteChannelMsgAPI(conf, msg_id).delete()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
