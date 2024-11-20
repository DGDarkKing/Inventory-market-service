from sqlalchemy.orm import selectinload

from joins.sa_join import SaJoinSpecification
from models import CameraOrm


# INTEGRATION_TEST
class JoinZone(SaJoinSpecification):
    def __init__(self):
        super().__init__(selectinload(CameraOrm.zone))
