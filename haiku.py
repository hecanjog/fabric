import fabric.fabric as dsp
import math

dsp.timer('start') 
dsp.seed('rhythm variation')

# Rhythm variation

etypes = ['phasor','line','impulse','saw','tri','flat']

tlen = dsp.stf(30)
tonic = 222.0

divisions = [ tlen / i for i in range(31,61) ]

rhythms = []

for i,d in enumerate(divisions):
    numbleeps = tlen / d + (tlen % d)
    freq = tonic * i 
    tone = dsp.tone(d, freq)
    bleeps = [ dsp.cut(tone, 0, dsp.mstf(dsp.randint(d * 0.1, d * 0.75))) for i in range(numbleeps) ]
    bleeps = [ dsp.env(b, dsp.randchoose(etypes), True) for b in bleeps ]
    bleeps = [ dsp.pad(b, 0, d - dsp.flen(b)) for b in bleeps ]
    bleeps = [ dsp.pan(b, dsp.rand(0.0,1.0)) for b in bleeps ]

    rhythms += [ ''.join(bleeps) ]

out = dsp.mix(rhythms)

print dsp.write(out, 'haiku-12-02-11-rhythm-variation', False)

dsp.timer('stop')
