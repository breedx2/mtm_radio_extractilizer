#!/usr/bin/env python
import argparse
import os
import subprocess

parser = argparse.ArgumentParser()

parser.add_argument("infile", help="the input file containing video files, one per line")
parser.add_argument("-n", "--numfiles", default="48", help="number of files per dir (defualt=48)")
parser.add_argument("-o", "--outdir", default="output", help="output dir (default=output)")
args = parser.parse_args()

if(os.path.isdir(args.outdir)):
    print("Output dir exists, skipping creation")
else:
    print("Making dir %s" % (args.outdir))
    os.mkdir(args.outdir)

print("Reading input file %s" % (args.infile))
with open(args.infile) as f:
    filenames = f.readlines()
filenames = map(lambda x: x.strip(), filenames)

print("Read %d filenames from %s" % (len(filenames), args.infile))
for filename in filenames:
    print("Extracting from %s" %(filename))
    # avconv -i tears_of_steel.mkv -map 0:2 -acodec libmp3lame -ar 44100 -ac 2 -ab 192k tears_of_steel_soundtrack.mp3
    # https://ffmpeg.org/ffmpeg-filters.html#silenceremove
    outfile = "%s/out.wav" %(args.outdir)
    cmd = "ffmpeg -i %s -acodec pcm_s16le -ar 44100 -ac 1 -af silenceremove=0:0:0:-1:0.5:-50dB -y %s" % (filename, outfile)
    #cmd = "ffmpeg -acodec pcm_s16le -ac 1 -i %s -o %s -y" % (filename, outfile)

    #ffmpeg -i o2/out.wav -af volumedetect -f null /dev/null 2>&1 | grep max_volume | awk '{ print $5 }'

    print(cmd)
    subprocess.check_call(cmd)
