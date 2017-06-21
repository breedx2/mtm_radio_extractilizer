# What?

A tool to extract audio files for use with the Music Thing Modular
Radio Music.  https://github.com/TomWhitwell/RadioMusic

Feed it a file full of video files, and it will extract the audios
into wav format and distribute them (in order) into a set of directories.

# Setup

## Prerequsites

* ffmpeg - must be in $PATH

## App/python

Probably want some virtualenv:

```
$ virtualenv env
$ source env/bin/activate

```

# Usage

tbd

# Limitations

Multi-language streams aren't really supported yet.  I suppose it just uses the first stream.
This could be fixed by another argument in the input file(??)
