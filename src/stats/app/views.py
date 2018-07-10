from aiohttp import web
import json
from playhouse.shortcuts import model_to_dict
from app.services import get_stat as get_stat_service
import asyncio


async def get_stat(request):
    loop = asyncio.get_event_loop()
    try:
        account = request.match_info.get('account', 'account_0@example.com')
        stats = await get_stat_service(account)
        res = [_stat for _stat in stats]

        return web.Response(
            text=json.dumps(res),
            status=200
        )
    except Exception as e:
        response = {
            'status': 'error',
            'explain': e
        }
        return web.Response(
            text=json.dumps(response),
            status=500
        )
