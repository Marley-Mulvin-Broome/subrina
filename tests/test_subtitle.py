from subrina import Subtitle
from subrina.subtime import srt_time


def test_srt_start_time():
    subtitle = Subtitle(["wow"], 0, 100)

    assert subtitle.srt_start_time == srt_time(0)


def test_srt_end_time():
    subtitle = Subtitle(["Wow!"], 0, 100)

    assert subtitle.srt_end_time == srt_time(100)
