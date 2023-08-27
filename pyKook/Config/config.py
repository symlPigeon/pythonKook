class accountConfig:
    def __init__(self, tokenType: str, token: str, i18N: str):
        assert tokenType == "Bot" or tokenType == "Bearer", "Invalid token type, must be 'Bot' or 'Bearer'!"
        self._tokenType = tokenType
        self._token = token
        self._i18n = i18N

    def getAuthToken(self):
        return "{} {}".format(self._tokenType, self._token)

    def getLang(self):
        return self._i18n