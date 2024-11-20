from conditions.interfaces.base_specification import SqlAlchemySpecification
from models import HaulOrm

# INTEGRATION_TEST

class HaulByZoneId(SqlAlchemySpecification):
    def __init__(self, zone_id):
        super().__init__(HaulOrm.zone_id == zone_id)


# INTEGRATION_TEST
class HaulById(SqlAlchemySpecification):
    def __init__(self, id):
        super().__init__(HaulOrm.id == id)
