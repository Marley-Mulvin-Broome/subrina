import pytest

from subrina.parsers.srtparser import SrtParser
from subrina import Subtitle
from subrina.subtitlerror import SubtitleError

srt_contents_data = [
    ("", []),
    ("""1
00:00:00,000 --> 00:00:01,000
Hello, world!
""", [Subtitle(["Hello, world!"], 0, 1000)]),
    ("""1
00:00:00,000 --> 00:00:01,000
Hello, world!

2
00:00:01,000 --> 00:00:02,000
Goodbye, world!
    """, [Subtitle(["Hello, world!"], 0, 1000), Subtitle(["Goodbye, world!"], 1000, 2000)]),
]

@pytest.fixture
def srt_parser() -> SrtParser:
    parser = SrtParser()
    parser.report_warnings = False
    return parser


@pytest.mark.parametrize("srt_contents,expected_subtitles", srt_contents_data)
def test_srt_parser(srt_contents, expected_subtitles, srt_parser):
    subtitles = []

    for subtitle in srt_parser.read(srt_contents):
        subtitles.append(subtitle)

    assert subtitles == expected_subtitles


@pytest.mark.parametrize("srt_contents,expected_subtitles", srt_contents_data)
def test_srt_parser_file(srt_contents, expected_subtitles, tmp_path, srt_parser):
    file_path = tmp_path / "test.srt"
    file_path.write_text(srt_contents)

    subtitles = list(srt_parser.read(file_path))

    assert subtitles == expected_subtitles


@pytest.mark.parametrize("srt_contents,expected_subtitles", srt_contents_data)
def test_srt_parser_file_stream(srt_contents, expected_subtitles, tmp_path, srt_parser):
    file_path = tmp_path / "test.srt"
    file_path.write_text(srt_contents)

    with open(file_path, "r") as f:
        subtitles = list(srt_parser.read(f))

        assert subtitles == expected_subtitles


@pytest.mark.parametrize("srt_contents,expected_subtitles", srt_contents_data)
def test_srt_parser_file_encoding(srt_contents, expected_subtitles, tmp_path, srt_parser):
    file_path = tmp_path / "test.srt"
    file_path.write_text(srt_contents, encoding="ascii")

    subtitles = list(srt_parser.read(file_path, encoding="ascii"))

    assert subtitles == expected_subtitles


@pytest.mark.parametrize("srt_contents,expected_subtitles", srt_contents_data)
def test_srt_parser_file_stream_encoding(srt_contents, expected_subtitles, tmp_path, srt_parser):
    file_path = tmp_path / "test.srt"
    file_path.write_text(srt_contents, encoding="ascii")

    with open(file_path, "r", encoding="ascii") as f:
        subtitles = list(srt_parser.read(f))

        assert subtitles == expected_subtitles


invalid_subtitle_data = [
    ("""1
     Not time
        """, SubtitleError),
    ("""Not number lol
00:00:00,000 --> 00:00:01,000
Crazy!""", SubtitleError),
]


@pytest.mark.parametrize("srt_contents,expected_exception", invalid_subtitle_data)
def test_srt_parser_invalid(srt_contents, expected_exception, srt_parser):
    with pytest.raises(expected_exception):
        list(srt_parser.read(srt_contents))
