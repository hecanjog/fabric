import dsp

dsp.timer('start')
dsp.seed('lifting')

# Back to basics.

etypes = ['line', 'sine', 'gauss', 'phasor', 'cos']

def stream(partial):
    around = dsp.tone(dsp.stf(3), 222 * partial)
    around = dsp.split(around, 0, 2)

    dsp.audio_params[0] = 1
    within = dsp.cycle(777)
    around = [''.join([a + within * dsp.randint(2, 64) for a in aa]) for aa in around]
    dsp.audio_params[0] = 2 

    return dsp.env(dsp.mixstereo(around), dsp.randchoose(etypes))

out = dsp.mix([stream(i) for i in range(1,5)])

print dsp.write(out, 'haiku-12-02-24-lifting', False)
dsp.timer('stop')
