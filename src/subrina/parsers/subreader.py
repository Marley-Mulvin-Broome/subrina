from abc import ABCMeta, abstractmethod
from typing import TextIO
from ..subtitle import Subtitle
from pathlib import Path


class ISubReader(metaclass=ABCMeta):
    @abstractmethod
    def read(self, path: [str | TextIO | Path], encoding="utf-8") -> list[Subtitle]:
        pass
