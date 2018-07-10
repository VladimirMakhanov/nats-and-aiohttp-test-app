import asyncio
import os
import aiohttp
from app import logger


async def get_data(account: str):
    url = os.getenv('REQUEST_URL')
    # account = account.encode('utf-8')
    async with aiohttp.ClientSession() as session:
        async with session.get(url=f"{url}/{account}/") as response:
            res = await response.text()
            logger.error(f"{url}/{account}/")
            logger.error(res)
            return res
