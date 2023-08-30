import asyncio

from IGNORE_ME import token
from pyKook.App.Bot import Bot
from pyKook.Config import accountConfig, botConfig

accountConf = accountConfig("Bot", token, "zh-CN")
botConf = botConfig(
    command=".",
    superusers=["2543244856"],
    plugin_enable=True,
    plugin_path="test/plugins/",
    exclude_plugins=["delete", "test.eventIgnoreMe"],
    use_plugin_cmd=True,
)
bot = Bot({"accountConfig": accountConf, "botConfig": botConf})


async def main():
    await bot.initialize()


asyncio.run(main())
