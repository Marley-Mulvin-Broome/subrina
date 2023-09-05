from dataclasses import dataclass
from .subtime import srt_time


@dataclass
class Subtitle:
    text: str
    """The text content of the subtitle"""
    start_time: int
    """Start time of the subtitle in ms"""
    end_time: int
    """End time of the subtitle in ms"""

    @property
    def srt_start_time(self) -> str:
        """Returns the start time in the srt format"""
        return srt_time(self.start_time)

    @property
    def srt_end_time(self) -> str:
        """Returns the end time in the srt format"""
        return srt_time(self.end_time)
