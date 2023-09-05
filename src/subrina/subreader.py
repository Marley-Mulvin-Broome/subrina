from abc import ABC, abstractmethod
from .formats import SubtitleFormat
from typing import TextIO


class ISubReader(metaclass=ABC):
    @abstractmethod
    def read(self, path: [str | TextIO], encoding="utf-8"):
        pass

    @abstractmethod
    def write(self, path: [str | TextIO], encoding="utf-8"):
        pass
