import asyncio
import os
from app import nc, loop
from app.services import get_data
import logging

logger = logging.getLogger()


async def connect():
    mq = os.getenv('MQ_SERVICE')

    await nc.connect(
        io_loop=loop,
        servers=[mq],
    )


async def handler(msg):
    logger.error('handle it!')
    # data = msg.data.decode()
    try:
        response = str(await get_data(msg.data.decode()))
        # logger.error(response)
        await nc.publish(msg.reply, response.encode())
    except Exception as e:
        logger.error(e)


async def subscribe():
    subject = os.getenv('SUBJECT_NAME')
    logger.error(subject)
    sid = await nc.subscribe(subject, subject, handler)


if __name__ == '__main__':
    logger.error('start')
    try:
        asyncio.ensure_future(connect(), loop=loop)
        asyncio.ensure_future(subscribe(), loop=loop)
        loop.run_forever()
    # except KeyboardInterrupt:
    #     pass
    #
    except Exception as e:
        logger.exception(e)
        logger.error(e)
    finally:
        logger.error('Complete')