#!/usr/bin/env python
import argparse
import os
from ffmpeg_util import *

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
filenames = filter(lambda x: not x.startswith('#'), filenames)

print("Read %d filenames from %s" % (len(filenames), args.infile))
filenum = 1
for filename in filenames:
    print("Extracting from %s" %(filename))
    extracted = "%s/out%d.wav" % (args.outdir, filenum)
    #extract_audio(filename, extracted)
    normalized = "%s/out%d_normalized.wav" % (args.outdir, filenum)
    normalize_audio(extracted, normalized)
    filenum = filenum + 1
