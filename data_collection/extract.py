import asyncio 
import logging
import os
from rnet import Impersonate, Client, Proxy, BlockingClient
from tenacity import (
    before_log,
    retry,
    stop_after_attempt,
    wait_exponential,
    before_log,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Extractor:
    def __init__(self):
        self.proxy = os.getenv("proxy")
        if not self.proxy:
            raise Exception("No proxy found")
        self.session = Client()
        self.session.update(
            impersonate=Impersonate.Firefox136,
            proxies=[Proxy.http(self.proxy), Proxy.https(self.proxy)],
        )
        self.blocking = BlockingClient()
        self.blocking.update(
            impersonate=Impersonate.Firefox136,
            proxies=[Proxy.http(self.proxy), Proxy.https(self.proxy)],
        )

    @retry(
        stop=stop_after_attempt(5),
        wait=wait_exponential(multiplier=1, min=3, max=10),
        before=before_log(logger, logging.INFO),
    )
    def extract_players(self, url):
        logger.info(f"Fetching URL: {url}")
        resp=self.blocking.get(url)
        if resp.status != 200:
            raise Exception(resp.status)
        return resp.text()
    
    def extract_player_data(self, url):
        logger.info(f"Extracting player data from {url}")
        resp=self.blocking.get(url)
        if resp.status != 200:
            raise Exception(resp.status)
        return resp.text()


if __name__ == "__main__":
