from aiohttp import web
import asyncio
from nats.aio.client import Client as NATS
import logging


app = web.Application()
loop = asyncio.get_event_loop()  # Note: custom loop!
nc = NATS()
logger = logging.getLogger()

