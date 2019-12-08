from srtoffset import SubtitlesFile, SubtitleTime


def test_parse_subtitle_file(subtitle_file, subtitle):
    subfile = SubtitlesFile.from_file(subtitle_file)
    assert subfile.subtitles[0] == subtitle


def test_subtitle_file_str(subtitle_file, subtitle_file_str):
    subfile = SubtitlesFile.from_file(subtitle_file)
    assert str(subfile) == subtitle_file_str


def test_subtitle_file_add_offset(subtitle_file):
    subfile = SubtitlesFile.from_file(subtitle_file)
    subfile += SubtitleTime(0, 0, 1, 0)
    assert subfile.subtitles[0].start_time == SubtitleTime(0, 0, 2, 600)
    assert subfile.subtitles[0].end_time == SubtitleTime(0, 0, 5, 200)
