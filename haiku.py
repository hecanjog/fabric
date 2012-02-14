import fabric.fabric as dsp

dsp.timer('start') 
dsp.seed('together')

# Coming together

curves = [dsp.wavetable('line', 1000 + dsp.randint(0,500)) for i in range(100)]
curves = [[int(dsp.mstf(10) + (i * dsp.mstf(190))) for i in c] for c in curves]

tonic = 100

tones = []
for i,c in enumerate(curves):
    pitch = tonic * (i+1)
    tone = dsp.tone(dsp.mstf(200), pitch)
    c = [dsp.cut(tone, 0, bleep) for bleep in c]
    c = [dsp.env(bleep, 'phasor') for bleep in c]
    c = [dsp.pan(bleep, dsp.rand()) for bleep in c]
    tones += [ ''.join(c) ]

out = dsp.mix(tones, False)

print dsp.write(out, 'haiku-12-02-13-together', False)

dsp.timer('stop')
