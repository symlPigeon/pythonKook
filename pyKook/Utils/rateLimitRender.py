import logging


class rateLimitRender:
    def __init__(self):
        self._rateLimit = None
        self._rateLimitRemaining = None
        self._rateLimitReset = None
        self._rateLimitBucket = None
        self._rateLimitGlobal = None
        self._status = False
    def update(self, header: dict):
        try:
            self._rateLimit = header["X-Rate-Limit-Limit"]
            self._rateLimitRemaining = header["X-Rate-Limit-Remaining"]
            self._rateLimitReset = header["X-Rate-Limit-Reset"]
            self._rateLimitBucket = header["X-Rate-Limit-Bucket"]
            self._rateLimitGlobal = header["X-Rate-Limit-Global"]
            self._status = True
            logging.warning(
                "Rate limit information detected! Rate limit: {}, Remaining: {}, Reset: {}, Bucket: {}, Global: {}".format(
                    self._rateLimit, self._rateLimitRemaining, self._rateLimitReset, self._rateLimitBucket,
                    self._rateLimitGlobal))
        except KeyError as e:
            # 没有速率限制信息，太棒啦
            self.reset()

    def reset(self):
        self._rateLimit = None
        self._rateLimitRemaining = None
        self._rateLimitReset = None
        self._rateLimitBucket = None
        self._rateLimitGlobal = None
        self._status = False
