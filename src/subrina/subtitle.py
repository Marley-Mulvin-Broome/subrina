from dataclasses import dataclass
from .subtime import srt_time


@dataclass(eq=False)
class Subtitle:
    lines: list[str]
    """The text content of the subtitle"""
    start_time: int
    """Start time of the subtitle in ms"""
    end_time: int
    """End time of the subtitle in ms"""

    def __eq__(self, other):
        if not isinstance(other, Subtitle):
            return False

        return (
            self.text == other.text
            and self.start_time == other.start_time
            and self.end_time == other.end_time
        )

    @property
    def srt_start_time(self) -> str:
        """Returns the start time in the srt format"""
        return srt_time(self.start_time)

    @property
    def srt_end_time(self) -> str:
        """Returns the end time in the srt format"""
        return srt_time(self.end_time)

    @property
    def text(self) -> str:
        """Returns the text of the subtitle"""
        return "\n".join(self.lines)

    def add_text(self, text: str):
        """Adds text to the subtitle"""
        self.lines.append(text.strip())
