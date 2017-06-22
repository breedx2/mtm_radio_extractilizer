
import subprocess
import re

def extract_audio(stream, infile, outfile):
    print("Extracting from %s" %(infile))
    cmd = ["ffmpeg", "-hide_banner", "-probesize", "250M", "-analyzeduration", "250M",
        "-i", infile, "-acodec", "pcm_s16le", "-ar", "44100"]
    if(stream != 0):
        cmd = cmd + ["-map", "0:%d" %(stream)]
    cmd = cmd + ["-ac", "1", "-af", "silenceremove=0:0:0:-1:0.5:-50dB", "-y", outfile]
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
