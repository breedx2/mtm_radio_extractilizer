
import subprocess

# avconv -i tears_of_steel.mkv -map 0:2 -acodec libmp3lame -ar 44100 -ac 2 -ab 192k tears_of_steel_soundtrack.mp3
# https://ffmpeg.org/ffmpeg-filters.html#silenceremove

#ffmpeg -i o2/out.wav -af volumedetect -f null /dev/null 2>&1 | grep max_volume | awk '{ print $5 }'
#ffmpeg -i o2/out.wav -af "volume=12.3dB" o2/norm.wav

#cmd = "ffmpeg -acodec pcm_s16le -ac 1 -i %s -o %s -y" % (filename, outfile)

def extract_audio(infile, outfile):
    print("Extracting from %s" %(infile))
    cmd = ["ffmpeg", "-hide_banner", "-i", infile, "-acodec", "pcm_s16le", "-ar", "44100",
        "-ac", "1", "-af", "silenceremove=0:0:0:-1:0.5:-50dB", "-y", outfile]
    print(' '.join(cmd))
    subprocess.check_call(cmd)
