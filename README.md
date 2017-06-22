# What?

A tool to extract audio files for use with the Music Thing Modular
Radio Music.  https://github.com/TomWhitwell/RadioMusic

Feed it a file full of video files, and it will extract the audios
into wav format and distribute them (in order) into a set of directories.

# Setup

## Prerequsites

* python - I used 2.7.13
* ffmpeg - must be in $PATH
* some video files you want to extract audio from

# Input file format

Prepare an input text file that tells the extractilizer what audios you want to extract.
The format is one file per line.  You can optionally specify an audio stream number
and a colon at the beginning of the file.  It might look like this:

```
/home/videos/nuclear_tests.mkv
/home/videos/my_birthday.avi
4:/home/videos/big_buck_bunny.iso
/home/video/performance_art.ogg
```

Note that the 3rd file specifies the audio stream 3 from the dvd, which might be a specific
language that you want.

# Usage

```
usage: extractilizer.py [-h] [-m MINUTES] [-o OUTDIR] infile

positional arguments:
  infile                the input file containing video files, one per line

optional arguments:
  -h, --help            show this help message and exit
  -m MINUTES, --minutes MINUTES
                        minutes per split output file (default = 10)
  -o OUTDIR, --outdir OUTDIR
                        output dir (default=output)
```

## Example

```
$ ./extractilizer.py -m 15 -o o2 files.txt
```

# How it works

For each file in the input file:
* Extract the audio stream to a file
 * Remove all silence below -50dB for 0.5 seconds
* Normalize audio by amplifying the peak to 0dB
* Split the normalized file into chunks of <n> minutes

filesystem layout/org tbd

# Limitations/improvements

* Can only extract one audio stream per video file.
* Does it also work with audio files as input?  Not sure, but would/could be useful.
* Parameters around silence detection are hard-coded, should make parametric
* Crashes hard -- could be made more flexible/recoverable/resumable
* Volume normalization is very basic, and increases the noise floor?  Maybe some users would like one of the more sophisticated/dynamic normalizers?

Please fork me and make me better!
