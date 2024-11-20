from models import HaulOrm
from orders.sa_order import SaOrderSpecification, null_first_order


# INTEGRATION_TEST
class HaulTimeDesc(SaOrderSpecification):
    def __init__(self, null_first: bool = False):
        super().__init__(null_first_order(HaulOrm.created_at, null_first).desc())
