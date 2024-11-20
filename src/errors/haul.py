class HaulNotCompleted(Exception):
    def __init__(self, id):
        self.id = id


class LastCompletedHaulIsNotCooldown(Exception):
    def __init__(self, id):
        self.id = id


class HaulNotFound(Exception):
    def __init__(self, id):
        self.id = id
