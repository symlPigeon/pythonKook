from pyKook.App.Bot import Bot
from pyKook.App.Object import Message

bot: Bot


@bot.on_event("isMentioned.atMe")
async def eventIsMentioned(msg: Message):
    channel = msg.getChannel()
    sender = msg.getAuthorId()
    await bot.sendRichText(channel, "(met){}(met)你at你马呢？".format(sender))


@bot.on_command("ignore_me")
async def eventIgnoreMe(msg: Message):
    channel = msg.getChannel()
    sender = msg.getAuthorId()
    await bot.sendRichText(channel, "Nothing happened.".format(sender))
