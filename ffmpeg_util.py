
import subprocess
import re

# avconv -i tears_of_steel.mkv -map 0:2 -acodec libmp3lame -ar 44100 -ac 2 -ab 192k some.mp3
# https://ffmpeg.org/ffmpeg-filters.html#silenceremove

#ffmpeg -i o2/out.wav -af volumedetect -f null /dev/null 2>&1 | grep max_volume | awk '{ print $5 }'
#ffmpeg -i o2/out.wav -af "volume=12.3dB" o2/norm.wav

# split
# ffmpeg -i somefile.mp3 -f segment -segment_time 3 -c copy out%03d.mp3

def extract_audio(infile, outfile):
    print("Extracting from %s" %(infile))
    cmd = ["ffmpeg", "-hide_banner", "-i", infile, "-acodec", "pcm_s16le", "-ar", "44100",
        "-ac", "1", "-af", "silenceremove=0:0:0:-1:0.5:-50dB", "-y", outfile]
    print(' '.join(cmd))
    subprocess.check_call(cmd)

def normalize_audio(infile, outfile):
    print("Normalizing audio in %s" %(infile))
    cmd = ["ffmpeg", "-hide_banner", "-i", infile, "-af", "volumedetect", "-f", "null", "/dev/null"]
    print(' '.join(cmd))
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    max = filter(lambda x: re.match(r'.*max_volume:.*', x), p.stderr)[0]
    max = re.sub(r'.*max_volume:\s+(.*) dB.*', r'\1', max)
    print("Increasing volume by %s" % (max))
    cmd = ["ffmpeg", "-i", infile, "-af", "volume=12.3dB", "-y", outfile]
    subprocess.check_call(cmd)

def split_file(infile, minutes, outprefix):
    print("Splitting audio in %s to %d minute chunks" %(infile, minutes))
    seconds = minutes * 60
    print(seconds)
    cmd = ["ffmpeg", "-hide_banner", "-i", infile, "-f", "segment",
        "-segment_time", "%d" %(seconds), "-c", "copy", "-y", "%s_%%03d.wav" %(outprefix)]
    print(' '.join(cmd))
    subprocess.check_call(cmd)
