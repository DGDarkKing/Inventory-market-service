class ZoneException(Exception):
    def __init__(self, number):
        self.number = number

    def __str__(self) -> str:
        return f"{self.__class__.__name__}. number: {self.number}"


class ZoneExists(ZoneException):
    def __init__(self, id, number, similar_zones=None):
        super().__init__(number)
        self.id = id
        self.similar_zones = similar_zones

    def __str__(self) -> str:
        result_text = f"{super().__str__()}; id: {self.id}"
        if self.similar_zones:
            similar_zones_text = ", ".join(
                [
                    f"(id: {zone.id}; number: {zone.recognize_result})"
                    for zone in self.similar_zones
                ]
            )
            result_text = f"{result_text}; similar zones: {similar_zones_text}"
        return result_text


class ZoneNotFound(ZoneException):
    pass


class ZoneCameraNotFound(ZoneException):
    pass


class ZoneHasCamera(ZoneException):
    def __init__(self, number, has_camera_id, additional_camera_id):
        super().__init__(number)
        self.has_camera_id = has_camera_id
        self.additional_camera_id = additional_camera_id

    def __str__(self) -> str:
        return f"{super().__str__()}; has camera_id: {self.has_camera_id}; {self.additional_camera_id}"
