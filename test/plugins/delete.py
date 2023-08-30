import logging
from pyKook.Utils.timer import Timer


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
