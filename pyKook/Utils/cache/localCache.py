from pyKook.Api.objects import User, Guild, Channel
from pyKook.Utils.singleton import singleton

# TODO: 持久化存储


@singleton
class cachedInfo:
    def __init__(self):
        self._user_cache = {}
        self._group_cache = {}
        self._channel_cache = {}

    def getUser(self, user_id: str) -> User | None:
        if user_id in self._user_cache:
            return self._user_cache[user_id]
        else:
            return None

    def getGroup(self, guild_id: str) -> Guild | None:
        if guild_id in self._group_cache:
            return self._group_cache[guild_id]
        else:
            return None

    def getChannel(self, channel_id: str) -> Channel | None:
        if channel_id in self._channel_cache:
            return self._channel_cache[channel_id]
        else:
            return None

    def addUser(self, user: User):
        self._user_cache[user.getId()] = user

    def addGroup(self, group: Guild):
        self._group_cache[group.getId()] = group

    def addChannel(self, channel: Channel):
        self._channel_cache[channel.getId()] = channel
