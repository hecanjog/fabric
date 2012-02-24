import dsp
import subprocess

# A very barebones haiku, but baby steps toward just-in-realtime 
# features for a performance at the end of March.
#
# Source sound by Meg Karls:
# http://sounds.hecanjog.com/violin-d.wav

dsp.timer('start') 
dsp.seed('rt')

violin = dsp.read('sounds/violin-d.wav')

def play(out=''):
    p = subprocess.Popen(['aplay', '-f', 'cd'], shell=False, stdin=subprocess.PIPE)
    p.communicate(out)
    
    return out

def ping(out=''):
    start = dsp.randint(0, dsp.flen(violin.data) - dsp.mstf(80))
    out += dsp.env(dsp.cut(violin.data, start, dsp.mstf(80)))

    return out

out = ''
for i in range(100):
    out += play(ping())

print dsp.write(out, 'haiku-12-02-23-rt', False)

dsp.timer('stop') 
