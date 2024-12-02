from faststream.rabbit import RabbitRouter

from utils.faststream_filters import TypeInIBodyFilter

router = RabbitRouter()
inventory_subscriber = router.subscriber(queue="inventory.queue")


@inventory_subscriber(filter=TypeInIBodyFilter("supply.added"))
async def add():
    # TODO
    pass


@inventory_subscriber(filter=TypeInIBodyFilter("supply.updated"))
async def update():
    # TODO
    pass
