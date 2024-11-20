class VehicleException(Exception):
    def __init__(self, number):
        self.number = number

    def __str__(self) -> str:
        return f"{self.__class__.__name__}. number: {self.number}"


class VehicleByIdNotFound(Exception):
    def __init__(self, id):
        self.id = id

    def __str__(self) -> str:
        return f"{self.__class__.__name__}. id: {self.id}"


class VehicleNotFound(VehicleException):
    pass


class VehiclesNotFound(Exception):
    pass


class VehicleNotFoundByTests(Exception):
    def __init__(self, tests: list[str]):
        self.tests = tests

    def __str__(self) -> str:
        return f"{self.__class__.__name__}. number: {self.tests}"
