import dsp

dsp.timer('start')
dsp.seed('alter')

# Alternating
#
# Violin by Meg Karls
# http://sounds.hecanjog.com/violin-e.wav

blocks = 100
violin = dsp.read('sounds/violin-e.wav')
curve = dsp.wavetable('vary', blocks)
lengths = [dsp.mstf(10) + (i * dsp.mstf(30)) for i in curve]

violins = dsp.split(violin.data, dsp.flen(violin.data) / blocks)

for i, violin in enumerate(violins):
    ppos = dsp.rand()
    violin = dsp.split(violin, lengths[i])
    violin = [dsp.env(v, 'sine', True) for v in violin]

    if i % 3 == 0:
        violin = [v for v in reversed(violin)]

    if i % 5 == 0:
        violin = [dsp.pad(v, 0, int(lengths[i] * 0.5)) for v in violin]

    violins[i] = [dsp.pan(v, ppos) for v in violin]

combine = [] 
for vi, violin in enumerate(violins):
    combine = dsp.interleave(violin, combine)

out = ''.join(combine)

print dsp.write(out, 'haiku-12-02-27-alter', False)
dsp.timer('stop')
