from sqlalchemy.orm import joinedload

from joins.sa_join import SaJoinSpecification
from models import ZoneOrm


# INTEGRATION_TEST
class JoinCamera(SaJoinSpecification):
    def __init__(self):
        super().__init__(joinedload(ZoneOrm.camera))
