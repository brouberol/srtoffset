from srtoffset import Subtitle, SubtitleTime


def test_subtitle_from_block(subtitle_block):
    sub = Subtitle.from_block(subtitle_block)
    assert sub.index == "1"
    assert sub.start_time == SubtitleTime(0, 0, 1, 600)
    assert sub.end_time == SubtitleTime(0, 0, 4, 200)


def test_subtitle_add_offset(subtitle):
    sub = subtitle + SubtitleTime(0, 0, 1, 0)
    assert sub.start_time == SubtitleTime(0, 0, 2, 600)
    assert sub.end_time == SubtitleTime(0, 0, 5, 200)


def test_subtitle_str(subtitle, subtitle_block_str):
    assert str(subtitle) == subtitle_block_str
