[![Build Status](https://travis-ci.org/brouberol/srtoffset.svg?branch=master)](https://travis-ci.org/brouberol/srtoffset) [![Coverage Status](https://coveralls.io/repos/github/brouberol/srtoffset/badge.svg?branch=master)](https://coveralls.io/github/brouberol/srtoffset?branch=master)

Apply a time offset to a subtitle .srt file.

Example:

```console
$ cat ~/example.srt
1
00:00:01,600 --> 00:00:04,200
English (US)

2
00:00:05,900 --> 00:00:07,999
This is a subtitle in American English

3
00:00:10,000 --> 00:00:14,000
Adding subtitles is very easy to do
$ srtoffset ~/example.srt '00:00:05,500'
1
00:00:07,100 --> 00:00:09,700
English (US)

2
00:00:11,400 --> 00:00:13,499
This is a subtitle in American English

3
00:00:15,500 --> 00:00:19,500
Adding subtitles is very easy to do
$ srtoffset ~/example.srt '00:00:01,000' --rewind
1
00:00:00,600 --> 00:00:03,200
English (US)

2
00:00:04,900 --> 00:00:06,999
This is a subtitle in American English

3
00:00:09,000 --> 00:00:13,000
Adding subtitles is very easy to do
```

## Setup the dev environment

```console
$ poetry install
```

## Run the tests

```console
$ poetry run pytest
```
