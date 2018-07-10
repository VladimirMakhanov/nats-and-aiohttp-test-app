from aiohttp import web
import asyncio

app = web.Application()
loop = asyncio.new_event_loop() # Note: custom loop!

