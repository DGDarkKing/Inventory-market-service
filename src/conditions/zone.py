from conditions.interfaces.base_specification import SqlAlchemySpecification
from models import ZoneOrm


# INTEGRATION_TEST
class ZoneByNumber(SqlAlchemySpecification):
    def __init__(self, number):
        super().__init__(ZoneOrm.number == number)


# INTEGRATION_TEST
class ZoneById(SqlAlchemySpecification):
    def __init__(self, id):
        super().__init__(ZoneOrm.id == id)
