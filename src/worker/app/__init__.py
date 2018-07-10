import asyncio
from nats.aio.client import Client as NATS
import requests
import asyncio_redis
import os
import logging

logger = logging.getLogger()
loop = asyncio.get_event_loop()
nc = NATS()
redis_url = os.getenv('REDIS_URL')
redis = asyncio_redis.Connection.create(
    host=redis_url,
    loop=loop
)
