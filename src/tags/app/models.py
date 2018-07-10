import asyncio
import peewee
import logging
import random
from collections import AsyncIterable
from peewee_async import Manager, PostgresqlDatabase
import asyncio

loop = asyncio.get_event_loop()

database = PostgresqlDatabase(
    'tags',
    user='tags_user',
    password='admin123',
    host='postgres'
)
objects = Manager(database, loop=loop)


class Tag(peewee.Model):
    id = peewee.IntegerField(primary_key=True, unique=True, index=True)
    account = peewee.CharField()
    campaign_id = peewee.IntegerField(index=True)
    tag = peewee.CharField()

    class Meta:
        database = database


objects.database.allow_sync = False


async def fill_table():
    """
    Вообще этой штуки тут быть не должно, стоило бы отдельно вынести.
    TODO: Вынести эту фигню в setup какой-нибудь.
    :return:
    """
    accounts = [f'account_{x}@example.com' for x in range(5)]
    campaigns = {
        'account_0@example.com': [1, 2, 3, 4, 5, ],
        'account_1@example.com': [6, 7, 8, 9, 10, ],
        'account_2@example.com': [11, 12, 13, 14, 15, ],
        'account_3@example.com': [16, 17, 18, 19, 20, ],
        'account_4@example.com': [21, 22, 23, 24, 25, ],
    }
    tags = [f'tag_{x}' for x in range(1, 6)]
    j = 1
    # campaign = 1
    for account in accounts:
        for campaign in campaigns[account]:
            for tag in random.sample(tags, k=random.randint(1, len(tags))):
                await objects.create(
                            Tag,
                            id=j,
                            account=account,
                            campaign_id=campaign,
                            tag=tag
                        )
                j += 1