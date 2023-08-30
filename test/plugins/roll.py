import logging


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
