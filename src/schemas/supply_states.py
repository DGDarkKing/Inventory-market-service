from enum import Enum


class SupplyState(str, Enum):
    ORDERED = "ordered"
    PENDING = "pending"
    CANCELED = "canceled"
    ACCEPTED = "accepted"
    EXPIRED = "expired"
