from pyKook.Config.config import accountConfig
from pyKook.Api.gateway.gateway import getGatewayAPI
from pyKook.Api.serverInterface.serverInfo import getUserGroupListAPI, getGroupInfoAPI

from IGNORE_ME import token # private information


conf = accountConfig("Bot", token, "zh-CN")
gateway = getGatewayAPI(conf)
print(gateway.getGateway())

groups = getUserGroupListAPI(conf).getData()
print(groups)

gid = groups[0]["id"]
ginfo = getGroupInfoAPI(conf, gid)
print(ginfo.getRoles())
print(ginfo.getChannels())
print(ginfo.getGroupInfo())