from aiohttp import web
import json
import asyncio
from app.services import check_account, collect_info


async def get_info(request):

    try:
        account = request.match_info.get('account', 'account_0@example.com')
        if check_account(account):
            response = await collect_info(account)
            return web.Response(
                text=json.dumps(response),
                status=200
            )

    except Exception as e:
        return web.Response(
            text=json.dumps(
                {
                    'status': 'error',
                    'explain': e
                }
            ),
            status=500
        )
