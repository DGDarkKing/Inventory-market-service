from schemas import Compress


class CompressionFail(Exception):
    def __init__(self, compress: Compress):
        self.compress = compress
