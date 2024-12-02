import asyncio

from faststream import FastStream
from faststream.rabbit import RabbitBroker

from settings import app_settings
from message_routers import *

broker = RabbitBroker(url=app_settings.amqp.url.unicode_string())
app = FastStream(
    broker=broker,
    title=app_settings.name,
)

broker.include_routers(
    goods_router,
    supply_router,
    trading_floor_router,
)


if __name__ == "__main__":
    asyncio.run(app.run())
