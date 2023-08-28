from pyKook.App.Bot import Bot
from pyKook.Config.config import accountConfig
import asyncio
from IGNORE_ME import token
from pyKook.Api.channelMessageInterface.channelMessage import sendChannelMsgAPI
import logging

accountConf = accountConfig("Bot", token, "zh-CN")
bot = Bot({"accountConfig": accountConf, "botConfig": {}})


@bot.on_event("isMentioned.atMe")
async def test(msg):
    logging.info("Test function called.")
    sendAPI = sendChannelMsgAPI(accountConf, msg.getChannel(), "Echo")
    await sendAPI.send()


async def main():
    await bot.initialize()


logging.getLogger().setLevel(logging.INFO)
asyncio.run(main())
