import dsp
import time
import sys

if len(sys.argv) > 1:
    notes = int(sys.argv[1])
else:
    notes = 1

violin = dsp.read('sounds/violin-d.wav')
vlen = dsp.flen(violin.data)
slen = dsp.mstf(280)
violin = [dsp.cut(violin.data, dsp.randint(0, vlen - slen), slen) for i in range(notes)]
scale = [0.5, 0.75, 0.938, 1.0, 2.0]

out = ''
for i,v in enumerate(violin): 
    if i < len(violin) / 2:
        v = dsp.transpose(v, dsp.randchoose(scale))
    
    v = dsp.env(dsp.pan(v, dsp.rand()), 'random')
    time.sleep(dsp.rand())
    
    out += dsp.play(v)
