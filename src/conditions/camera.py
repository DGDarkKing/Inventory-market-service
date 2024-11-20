from conditions.interfaces.base_specification import SqlAlchemySpecification
from models import CameraOrm

# INTEGRATION_TEST
class CameraById(SqlAlchemySpecification):
    def __init__(self, id):
        super().__init__(CameraOrm.id == id)
