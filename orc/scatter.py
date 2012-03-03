import dsp
import time
import sys

fixed = True
notes = 1

args = [arg for arg in sys.argv if arg != '']

if len(args) > 1:
    notes = int(args[1])

if len(args) > 2:
    dsp.seed(args[2])

violin = dsp.read('sounds/violin-d.wav')
vlen = dsp.flen(violin.data)
slen = dsp.mstf(dsp.randint(1, 2000))
violin = [dsp.cut(violin.data, dsp.randint(0, vlen - slen), slen) for i in range(notes)]
scale = [0.5, 1.0, 2.0, 3.0]

out = ''
for i,v in enumerate(violin): 
    if i < len(violin) / 2:
        v = dsp.transpose(v, dsp.randchoose(scale))
    
    v = dsp.env(dsp.pan(v, dsp.rand()), 'random')
    time.sleep(dsp.rand(0.0, 0.2))
    
    out += dsp.play(v)
