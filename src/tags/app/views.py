from aiohttp import web
import json
from playhouse.shortcuts import model_to_dict
from app.services import get_tags as get_tags_service
import asyncio


async def get_tags(request):
    loop = asyncio.get_event_loop()
    try:
        account = request.match_info.get('account', 'account_0@example.com')
        tags = await get_tags_service(account)
        # res = [model_to_dict(stat) for stat in stats]
        res_tmp = {}

        # Группируем данные. Все больше думаю, что MongoDB тут была бы лучше. Если вообще нужна
        for tag in tags:
            if tag.campaign_id not in res_tmp.keys():
                res_tmp[tag.campaign_id] = [tag.tag]
            else:
                res_tmp[tag.campaign_id].append(tag.tag)

        # Приводим к итоговому виду
        res = []
        for campaign_id in list(res_tmp.keys()):
            tmp = dict()
            tmp['campaign_id'] = campaign_id
            tmp['tags'] = res_tmp[campaign_id]
            res.append(tmp)

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
