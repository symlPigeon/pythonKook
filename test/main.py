from pyKook.Config.config import accountConfig
from pyKook.Api.gateway.gateway import getGatewayAPI
from pyKook.Utils.websocketHandler import websocketHandler
from pyKook.Api.serverInterface.serverInfo import getGroupInfoAPI, getUserGroupListAPI

from IGNORE_ME import token  # private information
import asyncio


async def main():
    conf = accountConfig("Bot", token, "zh-CN")
    userGroupAPI = getUserGroupListAPI(conf)
    groupList = await userGroupAPI.getGroupIdList()
    groupInfoAPI = getGroupInfoAPI(conf, groupList[0])
    groupInfo = await groupInfoAPI.getGroupInfo()
    print(groupInfo)
    print(groupInfo.dump())
    channelInfo = await groupInfoAPI.getChannels()
    print(channelInfo)
    for chn in channelInfo:
        print(chn.dump())
    roleInfo = await groupInfoAPI.getRoles()
    print(roleInfo)
    for role in roleInfo:
        print(role.dump())


if __name__ == "__main__":
    asyncio.run(main())
