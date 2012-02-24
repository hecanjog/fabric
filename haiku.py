import dsp
import time
import sys

# A very barebones haiku, but baby steps toward just-in-realtime 
# features for a performance at the end of March.
#
# Source sound by Meg Karls:
# http://sounds.hecanjog.com/violin-d.wav

dsp.seed('sleep')

print sys.argv

violin = dsp.read('sounds/violin-d.wav')
vlen = dsp.flen(violin.data)
slen = dsp.mstf(280)
violin = [dsp.cut(violin.data, dsp.randint(0, vlen - slen), slen) for i in range(100)]
scale = [0.5, 0.75, 0.938, 1.0, 2.0]

out = ''
for i,v in enumerate(violin): 
    if i < len(violin) / 2:
        v = dsp.transpose(v, dsp.randchoose(scale))
    
    v = dsp.env(dsp.pan(v, dsp.rand()), 'random')
    time.sleep(dsp.rand())
    
    out += dsp.play(v)
