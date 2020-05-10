#!/usr/bin/env python3

"""
Script mutating a subtitles (.srt) file by applying a time offset to each subtitle.

Examples:
    % srtoffset movie.srt '00:00:31,500'
    % srtoffset movie.srt '00:00:03,125' --rewind
"""

import argparse
import os
import sys
import re


TIMING_PATTERN = re.compile(
    r"(?P<hours>\d{2}):(?P<minutes>\d{2}):(?P<seconds>\d{2}),(?P<ms>\d{3})"
)

TIME_SEPARATOR = " --> "


def parse_args():  # pragma: no cover
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("subtitles", help="The subtitles file to manipulate")
    parser.add_argument("offset", help="The offset to apply to the subtitles file")
    parser.add_argument(
        "--rewind",
        action="store_true",
        default=False,
        help="Apply a negative time offset to the subtitle timing",
    )
    parser.add_argument(
        "-i",
        "--inplace",
        action="store_true",
        default=False,
        help="Perform the translation in-place",
    )
    return parser.parse_args()


class SubtitlesFile:
    """A subtitle file"""

    def __init__(self, subtitles):
        self.subtitles = subtitles

    def __str__(self):
        """Render the whole subtitle file to a string"""
        str_subs = []
        for sub in self.subtitles:
            str_subs.append(str(sub))
        return "\n\n".join(str_subs)

    def __add__(self, offset):
        """Mutate each subtitle line in the file by applying the argument time offset"""
        for i, _ in enumerate(self.subtitles):
            self.subtitles[i] += offset
        return self

    @classmethod
    def from_file(cls, f):
        """Parse a .srt file into a list of Subtitle objects"""
        subtitles, block = [], []
        for line in f:
            line = line.strip()
            if line:
                block.append(line)
            else:
                subtitles.append(Subtitle.from_block(block))
                block = []
        if block:
            subtitles.append(Subtitle.from_block(block))
        return cls(subtitles)


class Subtitle:
    """A subtitle line"""

    @classmethod
    def from_block(cls, block):
        start_time, end_time = map(SubtitleTime.from_str, block[1].split(TIME_SEPARATOR))
        return cls(
            index=block[0],
            start_time=start_time,
            end_time=end_time,
            text=".\n".join(block[2:]),
        )

    def __init__(self, index, start_time, end_time, text):
        self.index = index
        self.start_time = start_time
        self.end_time = end_time
        self.text = text

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __add__(self, offset):
        """Implements adding a time offset to the Subtitle time interval."""
        self.start_time += offset
        self.end_time += offset
        return self

    def __str__(self):
        """Renders the whole subtitle block to a string"""
        return "{index}\n{start_time}{sep}{end_time}\n{text}".format(
            index=self.index,
            start_time=self.start_time,
            sep=TIME_SEPARATOR,
            end_time=self.end_time,
            text=self.text,
        )


class SubtitleTime:
    """Represents a subtitle start or end time"""

    @classmethod
    def from_str(cls, t_str, rewind=False):
        m = re.match(TIMING_PATTERN, t_str)
        if not m:
            raise ValueError
        d = m.groupdict()
        factor = -1 if rewind else 1
        return cls(
            hours=factor * int(d["hours"]),
            minutes=factor * int(d["minutes"]),
            seconds=factor * int(d["seconds"]),
            milliseconds=factor * int(d["ms"]),
        )

    def __init__(self, hours, minutes, seconds, milliseconds):
        self.hours = hours
        self.minutes = minutes
        self.seconds = seconds
        self.milliseconds = milliseconds

    def __repr__(self):  # pragma: no cover
        return "<{cls} {self_str}>".format(cls=self.__class__.__name__, self_str=str(self))

    def __str__(self):
        h = str(self.hours).zfill(2)
        m = str(self.minutes).zfill(2)
        s = str(self.seconds).zfill(2)
        ms = str(self.milliseconds).zfill(3)
        return "{0}:{1}:{2},{3}".format(h, m, s, ms)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __add__(self, offset):
        """Implements adding an offset time to the current SubtitleTime object."""
        extra_seconds, ms = divmod(self.milliseconds + offset.milliseconds, 1000)
        extra_minutes, seconds = divmod(self.seconds + offset.seconds + extra_seconds, 60)
        extra_hours, minutes = divmod(self.minutes + offset.minutes + extra_minutes, 60)
        hours = self.hours + offset.hours + extra_hours
        return self.__class__(hours, minutes, seconds, ms)


def main():  # pragma: no cover
    args = parse_args()
    if not os.path.exists(args.subtitles):
        print("{subtitles} file does not exist. Exiting.".format(subtitles=args.subtitles))
        sys.exit(1)

    try:
        time_offset = SubtitleTime.from_str(args.offset, rewind=args.rewind)
    except ValueError:
        print("Could not parse argument offset. Must be of form {hh}:{mm}:{ss},{ms}")
        sys.exit(1)

    subfile = SubtitlesFile.from_file(open(args.subtitles))
    subfile += time_offset

    if args.inplace:
        with open(args.subtitles, "w") as out:
            out.write(str(subfile))
            out.flush()
    else:
        print(str(subfile))
