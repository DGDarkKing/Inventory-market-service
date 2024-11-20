from sqlalchemy.orm import selectinload

from joins.sa_join import SaJoinSpecification
from models import HaulOrm


# INTEGRATION_TEST
class JoinDumpTrack(SaJoinSpecification):
    def __init__(self):
        super().__init__(selectinload(HaulOrm.vehicle))


# INTEGRATION_TEST
class JoinZone(SaJoinSpecification):
    def __init__(self):
        super().__init__(selectinload(HaulOrm.zone))
