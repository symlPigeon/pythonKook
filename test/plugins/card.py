import logging

from pyKook.App.Object import Card


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
