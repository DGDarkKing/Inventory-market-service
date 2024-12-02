from faststream.rabbit import RabbitRouter

from utils.faststream_filters import TypeInIBodyFilter

router = RabbitRouter()
inventory_subscriber = router.subscriber(queue="inventory.queue")


@inventory_subscriber(filter=TypeInIBodyFilter("goods.bought"))
async def buy():
    # TODO
    pass

