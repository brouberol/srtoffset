import pytest

from srtoffset import SubtitleTime


@pytest.mark.parametrize(
    "base_time,offset,expected",
    [
        [(0, 0, 0, 0), (0, 0, 1, 0), (0, 0, 1, 0)],
        [(0, 0, 0, 1), (0, 0, 1, 0), (0, 0, 1, 1)],
        [(0, 0, 1, 1), (0, 0, 1, 0), (0, 0, 2, 1)],
        [(0, 30, 0, 0), (0, 31, 0, 0), (1, 1, 0, 0)],
    ],
)
def test_add_positive_offset_to_subtitle_time(base_time, offset, expected):
    assert SubtitleTime(*base_time) + SubtitleTime(*offset) == SubtitleTime(*expected)


@pytest.mark.parametrize(
    "base_time,offset,expected",
    [
        [(0, 0, 2, 0), (0, 0, -1, 0), (0, 0, 1, 0)],
        [(0, 1, 0, 0), (0, 0, -1, 0), (0, 0, 59, 0)],
        [(1, 0, 0, 0), (0, -1, 0, 0), (0, 59, 0, 0)],
    ],
)
def test_add_negative_offset_to_subtitle_time(base_time, offset, expected):
    assert SubtitleTime(*base_time) + SubtitleTime(*offset) == SubtitleTime(*expected)


def test_subtitle_time_from_str():
    assert SubtitleTime.from_str("01:02:03,400") == SubtitleTime(1, 2, 3, 400)


def test_subtitle_time_from_str_rewind():
    assert SubtitleTime.from_str("01:02:03,400", rewind=True) == SubtitleTime(
        -1, -2, -3, -400
    )


def test_subtitle_time_from_str_no_match():
    with pytest.raises(ValueError):
        SubtitleTime.from_str("nope")


def test_subtitle_time_str():
    assert str(SubtitleTime(1, 2, 3, 400)) == "01:02:03,400"


def test_subtitle_time_equality():
    assert SubtitleTime(1, 2, 3, 400) == SubtitleTime(1, 2, 3, 400)
    assert SubtitleTime(1, 2, 3, 400) != SubtitleTime(0, 4, 0, 100)
