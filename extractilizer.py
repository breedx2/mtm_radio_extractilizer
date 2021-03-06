#!/usr/bin/env python
import argparse
import os
import shutil
import re
from ffmpeg_util import *
from card_builder import *

parser = argparse.ArgumentParser()

parser.add_argument("infile", help="the input file containing video files, one per line")
parser.add_argument("-m", "--minutes", default=10, type=int, help="minutes per split output file (default = 10)")
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
filenames = filter(lambda x: not x.startswith('#'), filenames)

def stream_from_filename(filename):
    if(re.match(r'^\d+:', filename)):
        return int(re.sub(r'^(\d+).*', r'\1', filename))
    return 0

def build_input(filename):
    stream = stream_from_filename(filename)
    return { 'filename': re.sub(r'^\d+:', '', filename), 'stream': stream }

input_items = map(build_input, filenames)

print("Read %d filenames from %s" % (len(input_items), args.infile))
tmpout = "%s/tmp" % (args.outdir)
shutil.rmtree(tmpout, True)
os.mkdir(tmpout)

filenum = 1
for input_item in input_items:
    print(input_item)
    print("Extracting stream %d from %s" % (input_item['stream'], input_item['filename']))
    extracted = "%s/out%03d.wav" % (tmpout, filenum)
    extract_audio(input_item['stream'], input_item['filename'], extracted)
    normalized = "%s/out%03d_normalized.wav" % (tmpout, filenum)
    normalize_audio(extracted, normalized)
    split_file(normalized, args.minutes, "%s/out%03d_split" % (tmpout, filenum))
    filenum = filenum + 1

prep_card_dir(args.outdir)
