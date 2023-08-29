from pyKook.App.Bot import Bot
from importlib.util import spec_from_file_location, module_from_spec


class pluginManager:
    def __init__(self, bot: Bot, path: str):
        """
        模组管理器
        :param bot: 要Bot对象，不是botAPI！！！
        :param path: 模组所在的路径，请以/结尾
        """
        self._bot = bot
        self._plugin_list = []
        self._path = path
        self._plugin_names = []

    def _loadPlugin(self, name: str):
        spec = spec_from_file_location(name, self._path + name + ".py")
        module = module_from_spec(spec)
        module.bot = self._bot
        spec.loader.exec_module(module)
        return module

    def _getPluginNames(self):
        # get all files in path
        import os

        filenames = os.listdir(self._path)
        for filename in filenames:
            if filename.endswith(".py"):
                self._plugin_names.append(filename[:-3])

    def _getAllFunc(self, module):
        import inspect

        return inspect.getmembers(module, inspect.isfunction)
