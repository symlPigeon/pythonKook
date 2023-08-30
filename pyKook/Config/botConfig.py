class botConfig:
    def __init__(self, **kwargs):
        self._command = kwargs.get("command", ".")
        self._superusers = kwargs.get("superusers", [])
        self._plugin_enable = kwargs.get("plugin_enable", False)
        self._plugin_path = kwargs.get("plugin_path", "plugins/")
        if self._plugin_path[-1] != "/":
            self._plugin_path += "/"
        self._exclude_plugins = kwargs.get("exclude_plugins", [])
        self._use_builtin_plugin_mgr = kwargs.get("use_plugin_cmd", True)

    def getCommand(self):
        return self._command

    def getSuperUsers(self):
        return self._superusers

    def isPluginEnable(self):
        return self._plugin_enable

    def getPluginPath(self):
        return self._plugin_path

    def getExcludePlugins(self):
        return self._exclude_plugins

    def isBuiltinCmdEnable(self):
        return self._use_builtin_plugin_mgr
