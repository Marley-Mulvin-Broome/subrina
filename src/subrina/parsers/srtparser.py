from .subreader import ISubReader
from ..subtitle import Subtitle
from typing import TextIO, Iterator
from ..subtitlerror import SubtitleError
from ..util import try_int, get_stream_from_argument
from ..subtime import srt_time_to_ms
from pathlib import Path
from ..subtitlewarning import SubtitleWarning
from warnings import warn


class SrtParser(ISubReader):
    _warnings: list[str] = []
    _current_subtitle = None
    _current_line = 0
    _expecting_time = False
    _done_subs = 0

    report_warnings = True

    def _push_current_subtitle(self) -> Subtitle | None:
        return_subtitle = self._current_subtitle
        if return_subtitle is not None:
            self._done_subs += 1

        self._current_subtitle = None
        self._expecting_time = False
        return return_subtitle

    def _start_subtitle(self, line) -> None:
        result = try_int(line.strip())

        if result is None:
            raise SubtitleError(
                f"Expected subtitle number @{self._current_line}th line of subtitle, got '{line}' instead"
            )

        if result != self._done_subs + 1:
            self._warn(
                f"Sub number on line {self._current_line} expected '{self._done_subs + 1}' but got '{result}'",
                1,
            )

        self._current_subtitle = Subtitle(lines=[], start_time=0, end_time=0)
        self._expecting_time = True

    def _parse_time(self, line) -> None:
        times = line.split("-->")

        if len(times) != 2:
            raise SubtitleError(
                f"Expected time range @{self._current_line}th line of subtitle, got '{line}' instead"
            )

        self._current_subtitle.start_time = srt_time_to_ms(times[0].strip())
        self._current_subtitle.end_time = srt_time_to_ms(times[1].strip())
        self._expecting_time = False

    def _parse_line(self, line) -> Subtitle | None:
        self._current_line += 1

        # empty line means end of subtitle
        if not line.strip():
            return self._push_current_subtitle()

        # if the current subtitle is None, then we are expecting a number
        if self._current_subtitle is None:
            return self._start_subtitle(line)

        if self._expecting_time:
            return self._parse_time(line)

        self._current_subtitle.add_text(line)

    def _warn(self, message: str):
        if self.report_warnings:
            warn(message, SubtitleWarning)

        self._warnings.append(message)

    def read(self, file: [str | TextIO | Path], encoding="utf-8") -> Iterator[Subtitle]:
        file_pointer = None

        try:
            file_pointer = get_stream_from_argument(file)

            if file_pointer is None:
                raise ValueError(f"Failed to open file @{file} -> {type(file_pointer)}")

            for line in file_pointer:
                result = self._parse_line(line)

                if result is not None:
                    yield result

            if leading_sub := self._push_current_subtitle():
                self._warn(
                    "Last subtitle in file isn't followed by an empty line (Subtitle terminator)"
                )
                yield leading_sub

        except UnicodeDecodeError as e:
            raise SubtitleError(f"Failed to decode file with unicode @{file}") from e

        except SubtitleError as e:
            raise SubtitleError(f"Failed to parse file @{file}") from e

        except ValueError as e:
            raise SubtitleError(f"Failed to open file @{file}") from e

        finally:
            if file_pointer is not None:
                file_pointer.close()
