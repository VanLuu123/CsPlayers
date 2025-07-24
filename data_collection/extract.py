import asyncio 
import logging
import os
from rnet import Impersonate, Client, Proxy
from tenacity import (
    before_log,
    retry,
    stop_after_attempt,
    wait_exponential,
)
from dotenv import load_dotenv 

load_dotenv()

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
        logger.info("Session Created.")

    @retry(
        stop=stop_after_attempt(5),
        wait=wait_exponential(multiplier=1, min=3, max=10),
        before=before_log(logger, logging.INFO),
    )
    async def fetch_html(self, url):
        logger.info(f"Async Requesting URL: {url}")
        resp = await self.session.get(url)
        if resp.status != 200:
            raise Exception(resp.status)
        return await resp.text()
        
    
    async def fetch_html_many(self, urls):
        res = await asyncio.gather(
            *[self.fetch_html(url) for url in urls],
            return_exceptions=True,
        )
        return res
