from .models import Stat
from .models import objects


async def get_stat(account: str):
    stats = await objects.execute(
        Stat.select(Stat.campaign_id, Stat.date, Stat.shows, Stat.clicks, Stat.costs).filter(Stat.account == account)
    )
    res = [
        {
            "campaign_id": stat.campaign_id,
            "date": stat.date,
            "shows": stat.shows,
            "clicks": stat.clicks,
            "costs": stat.costs,
        }
        for stat in stats
    ]
    return res
