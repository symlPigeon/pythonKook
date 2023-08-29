from pyKook.App.Bot import Bot
from pyKook.App.Object import Card
from pyKook.Config import accountConfig, botConfig
import asyncio
from IGNORE_ME import token
from pyKook.Api.channelMessageInterface.channelMessage import sendChannelMsgAPI
from pyKook.Utils.timer import Timer
import logging

accountConf = accountConfig("Bot", token, "zh-CN")
botConf = botConfig(command=".", superusers=["2543244856"])
bot = Bot({"accountConfig": accountConf, "botConfig": botConf})


@bot.on_event("isMentioned.atMe")
async def test(msg):
    logging.info("Test function called.")
    await bot.sendText(msg.getChannel(), "Hello, world!", reply=msg)


@bot.on_command("r")
async def roll(msg):
    logging.info("Roll function called.")
    logging.info("Msg: %s" % msg.content())
    import random

    contents = msg.content().lstrip(".r ").strip().split("d")
    try:
        l, r = contents
        l = int(l)
        r = int(r)
        dices = []
        for _ in range(l):
            dices.append(random.randint(1, r))
        ans = "".join(["%d+" % i for i in dices])[:-1] + "= {}".format(sum(dices))
        await bot.sendText(msg.getChannel(), ans, reply=msg)
    except:
        await bot.sendText(msg.getChannel(), "参数错误！", reply=msg)


@bot.on_command("card")
async def send_test_card(msg):
    logging.info("Card function called.")
    card = Card()
    card.addCard(theme="warning")
    card.addText("测试卡片")
    card.addTextWithButton(
        "测试链接",
        "点击我",
        button_action="link",
        button_value="https://www.bilibili.com/video/BV1GJ411x7h7/",
    )
    card.addDivider()

    async def _reply(msg, **args):
        await bot.sendRichText(
            msg.getChannel(), "傻逼(met){}(met)".format(msg.getAuthorId())
        )

    card.addTextWithButton(
        "测试链接2",
        "点击我2",
        button_action="return-val",
        button_value="after_clicked",
        callback=_reply,
        args={},
    )
    await bot.sendCardText(msg.getChannel(), card)


@bot.on_command("testDelete")
async def testDelete(msg):
    logging.info("Delete function called.")
    msg_id = await bot.sendText(msg.getChannel(), "本消息将在10秒后销毁", reply=msg)
    msg_sent = bot.getMessageById(msg_id)
    if not msg_sent:
        return
    timer = Timer(10, bot.deleteMessage, message=msg_sent)
    timer.start()


@bot.privileged("deleteAll")
async def deleteAll(msg):
    logging.info("Delete all function called.")
    messages = bot.getAllMessages()
    for message in messages:
        await bot.deleteMessage(message)


async def main():
    await bot.initialize()


logging.getLogger().setLevel(logging.INFO)
asyncio.run(main())
