import fabric.fabric as dsp
import math

dsp.timer('start') 
dsp.seed('driftless')

# let 100 partials bloom

partials = 100
tonic = 100.0
length = dsp.stf(60)

freqs = [ tonic * i for i in range(1, partials + 1) ]
durations = [ length / i + (length % i) for i in range(1, partials + 1) ]

bleeps = []
for i in range(partials):
    bleep = dsp.tone(dsp.mstf(100), freqs[i])
    if durations[i] > dsp.mstf(100):
        bleep = dsp.env(bleep, 'phasor', True)
        bleep = dsp.pad(bleep, 0, durations[i] - dsp.flen(bleep))
    else:
        bleep = dsp.cut(bleep, 0, durations[i])
        bleep = dsp.env(bleep, 'phasor', True)

    bleep = [ dsp.pan(bleep, dsp.rand()) for i in range(length / durations[i]) ]
    bleeps += [ ''.join(bleep) ]

out = dsp.mix(bleeps)

print dsp.write(out, 'haiku-12-02-11-driftless', False)

dsp.timer('stop')
