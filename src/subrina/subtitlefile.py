from .subtypes import SubtitleLike
from .subtitle import Subtitle

from .parsers import ISubReader, SrtParser


extension_to_reader = {"srt": SrtParser}


def get_reader(file_path: str) -> ISubReader:
    extension = file_path.split(".")[-1]

    if extension not in extension_to_reader:
        raise ValueError(f"Unsupported file type {extension}")

    return extension_to_reader[extension]()


class SubtitleFile:
    _parser: ISubReader = None

    subtitles: list[Subtitle] = []

    def __init__(self, file: SubtitleLike | None = None):
        if file is not None:
            self.parse(file)

    def parse(self, file: SubtitleLike, preserve_current_subtitles: bool = True):
        if self._parser is None:
            self._parser = SrtParser()
        if not preserve_current_subtitles:
            self.subtitles.clear()

        self.subtitles += self._parser.read(file)

    def write(self):
        raise NotImplementedError()
