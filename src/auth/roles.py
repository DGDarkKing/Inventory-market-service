from enum import Enum


class Roles(str, Enum):
    STOREKEEPER = "storekeeper"
    CASHIER = "cashier"
    MANAGER = "manager"
