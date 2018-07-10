import os
import json
from nats.aio.client import Client as NATS
from nats.aio.errors import ErrConnectionClosed, ErrTimeout, ErrNoServers
import redis
from app import loop, nc, logger

# nc.connect(
#     servers=['nats://nats:4222'],
#     io_loop=loop,
# )


def check_account(account: str):
    return True


async def get_info_from_services(account: str):
    # logger.error(f'get account {account}')
    mq = os.getenv('MQ_SERVICE')

    await nc.connect(
        servers=[mq],
        io_loop=loop,
    )

    campaigns_subject = os.getenv('CAMPAIGNS_SUBJECT_NAME')
    tags_subject = os.getenv('TAGS_SUBJECT_NAME')
    stats_subject = os.getenv('STATS_SUBJECT_NAME')

    campaigns = await nc.timed_request(campaigns_subject, account.encode(), 1)
    tags = await nc.timed_request(tags_subject, account.encode(), 1)
    stats = await nc.timed_request(stats_subject, account.encode(), 1)

    campaigns = json.loads(campaigns.data.decode())
    tags = json.loads(tags.data.decode())
    stats = json.loads(stats.data.decode())

    return campaigns, stats, tags


async def build_answer(campaigns: list, stats: list, tags: list):
    campaigns_dict = await campaigns_to_dict(campaigns)
    stats_dict = await stats_to_dict(stats)
    tags_dict = await tags_to_dict(tags)

    # logger.info([campaigns_dict, stats_dict, tags_dict])
    answer = []

    for campaign_id, campaign_title in campaigns_dict.items():
        answer_one = {
            'id': campaign_id,
            'title': campaign_title,
            'get_stat': [x for x in stats_dict[campaign_id]],
            'tags': tags_dict[campaign_id],
        }

        answer.append(answer_one)

    return answer
    # return campaigns_dict, stats_dict, tags_dict


async def campaigns_to_dict(campaigns: list):
    result = {}
    for camp in campaigns:
        result[camp['id']] = camp['title']
    return result


async def stats_to_dict(stats: list):
    # stats_list = json.loads(stats)
    result = {}

    for stat in stats:
        if stat['campaign_id'] in result.keys():
            result[stat['campaign_id']].append(
                {
                    'date': stat['date'],
                    'shows': stat['shows'],
                    'clicks': stat['clicks'],
                    'costs': stat['costs'],
                }
            )

        else:
            result[stat['campaign_id']] = [
                {
                    'date': stat['date'],
                    'shows': stat['shows'],
                    'clicks': stat['clicks'],
                    'costs': stat['costs'],
                }
            ]

    return result


async def tags_to_dict(tags: list):
    # tags_list = json.loads(tags)
    result = {}
    for tag in tags:
        result[tag['campaign_id']] = tag['tags']
    return result


async def collect_info(account: str):
    """
    Функция сбора
    :param account:
    :return:
    """
    try:
        campaigns, stats, tags = await get_info_from_services(account)
        result = await build_answer(campaigns, stats, tags)
        # logger.error(result)
        # return {
        #     'status': '200',
        #     'campaigns': campaigns,
        #     'stats': stats,
        #     'tags': tags,
        #     # 'result': result,
        # }
        # campaigns_result, stats_result, tags_result = await build_answer(campaigns, stats, tags)
        # return {
        #     'status': '200',
        #     'campaigns': campaigns_result,
        #     'stats': stats_result,
        #     'tags': tags_result,
        #     # 'result': result,
        # }

    except ErrTimeout as e:
        return {
            'status': '400',
            'error': str(e)
        }

    except Exception as e:
        return {
            'status': '1400',
            'error': str(e)
        }

    else:
        # return {
        #     'status': 200,
        #     'result': result,
        # }
        return result
