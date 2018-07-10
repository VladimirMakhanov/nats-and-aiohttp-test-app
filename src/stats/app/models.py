import asyncio
import peewee
import logging
import random
from collections import AsyncIterable
from peewee_async import Manager, PostgresqlDatabase
import asyncio

loop = asyncio.get_event_loop()

database = PostgresqlDatabase(
    'stats',
    user='stats_user',
    password='admin123',
    host='postgres'
)
objects = Manager(database, loop=loop)


class Stat(peewee.Model):
    id = peewee.IntegerField(primary_key=True, unique=True, index=True)
    account = peewee.CharField()
    campaign_id = peewee.IntegerField()
    date = peewee.CharField()
    shows = peewee.IntegerField()
    clicks = peewee.IntegerField()
    costs = peewee.IntegerField()

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
    j = 1
    dates = ['2018-05-24', '2018-05-25', '2018-05-26', '2018-05-27', '2018-05-28']
    shows = [50*i for i in range(1,20)]
    clicks = [2*i for i in range(1,20)]
    costs = [i for i in range(1,20)]
    for acc in accounts:
        for i in range(5):
            await objects.create_or_get(
                Stat,
                id=j+1,
                account=acc,
                campaign_id=j,
                date=dates[i],  # Плохой код, но почему бы и нет. Функция применится один раз, потом будет просто бекап базы )
                shows=random.choice(shows),
                clicks=random.choice(clicks),
                costs=random.choice(costs)
            )
            j += 1
