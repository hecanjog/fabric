import dsp

dsp.timer('start')
dsp.seed('inter')

# I read an interview with Ligeti last night discussing rhythm 

etypes = ['line', 'sine', 'gauss', 'phasor', 'cos']
curve = dsp.wavetable('sine', 100)
lengths = [dsp.mstf(100) + (i * dsp.mstf(100)) for i in curve]

sines = []
for length in lengths:
    tone = dsp.tone(int(length), 222 + 77 * dsp.randint(77), 'sine2pi', 0.4)
    tone = dsp.env(tone, dsp.randchoose(etypes), True)
    tone = dsp.pan(tone, dsp.rand())
    sines += [ tone ]

sines = [[sine] * 10 for sine in sines]
combine = ['' for i in range(10)]

for sine in sines:
    for snum, ss in enumerate(sine):
        combine[snum] += ss * dsp.randint(1, 3)

out = dsp.mix(combine)

print dsp.write(out, 'haiku-12-02-26-inter', False)
dsp.timer('stop')
