import pytest

from io import StringIO

from srtoffset import Subtitle

TEST_SUBTITLE = """1
00:00:01,600 --> 00:00:04,200
English (US)

2
00:00:05,900 --> 00:00:07,999
This is a subtitle in American English

3
00:00:10,000 --> 00:00:14,000
Adding subtitles is very easy to do"""


@pytest.fixture
def subtitle_file_str():
    return TEST_SUBTITLE


@pytest.fixture
def subtitle_file():
    return StringIO(TEST_SUBTITLE)


@pytest.fixture
def subtitle_blocks():
    return map(str.split("\n"), TEST_SUBTITLE.split("\n\n"))


@pytest.fixture
def subtitle_block():
    return TEST_SUBTITLE.split("\n\n")[0].split("\n")


@pytest.fixture
def subtitle_block_str():
    return TEST_SUBTITLE.split("\n\n")[0]


@pytest.fixture
def subtitle():
    return Subtitle.from_block(TEST_SUBTITLE.split("\n\n")[0].split("\n"))
