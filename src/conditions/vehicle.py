from conditions.interfaces.base_specification import SqlAlchemySpecification
from models import VehicleOrm


# INTEGRATION_TEST
class VehicleIsNotDeleted(SqlAlchemySpecification):
    def __init__(self):
        super().__init__(VehicleOrm.is_deleted == False)


# INTEGRATION_TEST
class VehicleByNumber(SqlAlchemySpecification):
    def __init__(self, number):
        super().__init__(VehicleOrm.number == number)


# INTEGRATION_TEST
class VehicleById(SqlAlchemySpecification):
    def __init__(self, id):
        super().__init__(VehicleOrm.id == id)
