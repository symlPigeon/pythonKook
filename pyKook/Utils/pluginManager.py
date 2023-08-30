from pyKook.Utils.loggingTool import logging

from pyKook.App.Bot import Bot
from pyKook.Config.botConfig import botConfig
from importlib.util import spec_from_file_location, module_from_spec


class pluginManager:
    def __init__(self, bot: Bot, config: botConfig):
        """
        模组管理器
        :param bot: 要Bot对象，不是botAPI！！！
        :param path: 模组所在的路径，请以/结尾
        """
        self._bot = bot
        self._enable = config.isPluginEnable()
        self._path = config.getPluginPath()
        self._exclude_plugins = config.getExcludePlugins()
        self._use_builtin = config.isBuiltinCmdEnable()
        self._module_list = {}
        self._module_funcs = {}
        self._exclude_modules = []
        self._exclude_functions = {}

    def _parse_exclude_list(self):
        for item in self._exclude_plugins:
            if "." in item:
                # exclude some function in a module
                module, func = item.split(".")
                if module not in self._exclude_functions:
                    self._exclude_functions[module] = [func]
                else:
                    self._exclude_functions[module].append(func)
            else:
                # exclude a module
                self._exclude_modules.append(item)

    def _loadPluginFile(self, name: str):
        spec = spec_from_file_location(name, self._path + name + ".py")
        module = module_from_spec(spec)
        module.bot = self._bot
        spec.loader.exec_module(module)
        return module

    def _loadPluginsNames(self):
        # get all files in path
        import os

        filenames = os.listdir(self._path)
        for filename in filenames:
            if filename.endswith(".py"):
                module_name = filename[:-3]
                logging.info(
                    "Found plugin file: {} {}".format(
                        filename,
                        "(excluded)" if module_name in self._exclude_modules else "",
                    )
                )
                if module_name not in self._exclude_modules:
                    self._module_list[module_name] = filename[:-3]

    def _getAllFunc(self, module):
        import inspect

        return inspect.getmembers(module, inspect.isfunction)

    def _loadFuncsInPlugin(self, module, excludes=None) -> list:
        if excludes is None:
            excludes = []
        plugin_funcs = []
        funcs = self._getAllFunc(module)
        for func in funcs:
            if func[1].__name__.startswith("decorated_on_event@"):
                try:
                    _, event_id, func_name = func[1].__name__.split("@")
                except ValueError as e:
                    logging.error("Error while parsing function name: {}".format(e))
                    logging.error("Function name: {}".format(func[1].__name__))
                    raise e
                logging.info(
                    "Found plugin function: {} in module {}".format(
                        func[1].__name__, module.__name__
                    )
                )
                if func_name not in excludes:
                    plugin_funcs.append(func)
                else:
                    logging.info("Excluded function: {}".format(func[1].__name__))
                    self._bot.unload_handler(event_id, func[1])
        return plugin_funcs

    def _unloadPlugin(self, module):
        module_name = module
        if module_name in self._module_list:
            logging.info("Unloading module {}...".format(module_name))
            for func in self._module_funcs[module_name]:
                self._bot.unload_handler(func[1].__name__.split("@")[1], func[1])
            del self._module_list[module_name]
            del self._module_funcs[module_name]
            self._exclude_modules.append(module_name)
            logging.info("Module {} unloaded.".format(module_name))

    def _loadPlugin(self, filename):
        logging.info("Loading functions in {}...".format(filename))
        module = self._loadPluginFile(filename)
        self._module_funcs[filename] = self._loadFuncsInPlugin(
            module, excludes=self._exclude_functions.get(filename, None)
        )
        if filename in self._exclude_modules:
            self._exclude_modules.remove(filename)
        if filename not in self._module_list:
            self._module_list[filename] = filename

    def load(self):
        if not self._enable:
            logging.info("Plugin manager disabled.")
            return
        if self._use_builtin:
            self._builtin_register_commands()
        self._parse_exclude_list()
        logging.debug("Exclude modules: {}".format(self._exclude_modules))
        logging.debug("Exclude functions: {}".format(self._exclude_functions))
        self._loadPluginsNames()
        for filename in self._module_list:
            self._loadPlugin(filename)
        logging.info("Plugins loaded.")

    def isEnabled(self):
        return self._enable

    def getModuleList(self):
        enable_list = list(self._module_list.values())
        disable_list = [name + "(disabled)" for name in self._exclude_modules]
        return enable_list + disable_list

    async def _plugin_mgr_builtin_list_modules(self, msg):
        text = "已加载的模组：\n"
        text += "\n".join(self.getModuleList())
        await self._bot.sendText(msg.getChannel(), text, reply=msg)

    async def _plugin_mgr_builtin_load_module(self, msg):
        module_name = msg.content()[1:].lstrip("plugin_load").strip()
        logging.info("User asked to load module: {}".format(module_name))
        if module_name in self._exclude_modules:
            self._loadPlugin(module_name)
            await self._bot.sendText(msg.getChannel(), "模组加载成功！", reply=msg)
        else:
            await self._bot.sendText(msg.getChannel(), "模组已经加载过了或者没有这个模组！", reply=msg)

    async def _plugin_mgr_builtin_unload_module(self, msg):
        module_name = msg.content()[1:].lstrip("plugin_unload").strip()
        if module_name in self._module_list:
            self._unloadPlugin(module_name)
            await self._bot.sendText(msg.getChannel(), "模组卸载成功！", reply=msg)
        else:
            await self._bot.sendText(msg.getChannel(), "模组未加载！", reply=msg)

    def _builtin_register_commands(self):
        logging.info("Registering pluginMgr builtin commands...")
        self._bot.load_handler(
            "command.plugin_list", self._plugin_mgr_builtin_list_modules
        )
        self._bot.load_handler(
            "command.plugin_load", self._plugin_mgr_builtin_load_module
        )
        self._bot.load_handler(
            "command.plugin_unload", self._plugin_mgr_builtin_unload_module
        )
        logging.info("PluginMgr builtin commands registered.")
