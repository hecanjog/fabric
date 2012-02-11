import fabric.fabric as dsp
import math

dsp.timer('start') 
dsp.seed('rhythm')

# Rhythm, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 

etypes = ['phasor','line','impulse','saw','tri','flat']

tlen = dsp.stf(30)
tonic = 293.7 / 2

divisions = [ tlen / i for i in range(1,301) ]

rhythms = []

for d in divisions:
    numbleeps = tlen / d + (tlen % d)
    freq = tonic * (1 + (1.0 / d))
    tone = dsp.tone(d, freq)
    bleeps = [ dsp.cut(tone, 0, dsp.mstf(dsp.randint(d * 0.1, d * 0.75))) for i in range(numbleeps) ]
    bleeps = [ dsp.env(b, dsp.randchoose(etypes), True) for b in bleeps ]
    bleeps = [ dsp.pad(b, 0, d - dsp.flen(b)) for b in bleeps ]
    bleeps = [ dsp.pan(b, dsp.rand(0.0,1.0)) for b in bleeps ]

    rhythms += [ ''.join(bleeps) ]

out = dsp.mix(rhythms)

print dsp.write(out, 'haiku-12-02-10-rhythm', False)

dsp.timer('stop')
