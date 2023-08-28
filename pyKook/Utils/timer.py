import asyncio
import logging


class Timer:
    def __init__(self, timeout: float, callback: callable, **args):
        self._timeout = timeout
        self._callback = callback
        self._task = None
        self._args = args
        logging.info("Timer {} created! Timeout: {}".format(id(self), timeout))

    def start(self):
        self._task = asyncio.ensure_future(self._job())
        logging.info("Timer {} started!".format(id(self)))

    async def _job(self):
        await asyncio.sleep(self._timeout)
        logging.info("Timer {} reached timeout!".format(id(self)))
        await self._callback(**self._args)
        self._task = None

    def cancel(self):
        if self._task:
            self._task.cancel()
            logging.info("Timer {} canceled!".format(id(self)))

    def refresh(self):
        self.cancel()
        self.start()
        logging.info("Timer {} refreshed!".format(id(self)))
