from dataclasses import dataclass


@dataclass
class SubtitleWarning(Warning):
    def __init__(self, *args, **kwargs):
        pass

    def __new__(cls, *args, **kwargs):
        pass
