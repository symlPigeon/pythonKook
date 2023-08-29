class botConfig:
    def __init__(self, **kwargs):
        self._command = kwargs.get("command", ".")
        self._superusers = kwargs.get("superusers", [])

    def getCommand(self):
        return self._command

    def getSuperUsers(self):
        return self._superusers
