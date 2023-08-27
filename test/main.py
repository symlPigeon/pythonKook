from pyKook.Config.config import accountConfig
from pyKook.Api.gateway.gateway import getGatewayAPI
from pyKook.Api.serverInterface.serverInfo import getUserGroupListAPI, getGroupInfoAPI
from pyKook.Api.channelInterface.channelMessage import sendChannelMsgAPI
from pyKook.Api.constants.messageType import MSG_TYPE

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

channel_id = "7380069416322298"
sender = sendChannelMsgAPI(conf, channel_id, "Hello World!", msg_type=MSG_TYPE.TEXT)
print(sender.send())
sender = sendChannelMsgAPI(conf, channel_id, "**Hello World!**", msg_type=MSG_TYPE.KMARKDOWN)
print(sender.send())