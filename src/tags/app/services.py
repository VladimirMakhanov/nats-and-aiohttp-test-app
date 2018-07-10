from .models import Tag
from .models import objects
from playhouse.shortcuts import model_to_dict


async def get_tags(account: str):
    tags = await objects.execute(
        Tag.select(Tag.campaign_id, Tag.tag).filter(Tag.account == account)
    )
    res = [tag for tag in tags]
    return res
