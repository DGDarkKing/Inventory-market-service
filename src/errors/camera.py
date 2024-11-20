class ExistingCameraBelongsAnotherZone(Exception):
    def __init__(self, id, zone_number):
        self.id = id
        self.zone_number = zone_number

    def __str__(self) -> str:
        return f'{self.__class__.__name__}: id: {self.id}; zone number: {self.zone_number}'
