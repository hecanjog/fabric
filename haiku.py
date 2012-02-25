import dsp

dsp.timer('start')
dsp.seed('gathering')

# Gathering toward 

etypes = ['line', 'sine', 'gauss', 'phasor', 'cos']

def stream(partial):
    around = dsp.pulsar(dsp.tone(dsp.stf(20), 444 * partial))
    around = dsp.split(around, 0, 2)

    within = dsp.tone(dsp.stf(20), 444 * (1.0 / partial))
    within = dsp.split(within, 0, 2)

    together = [''.join(dsp.interleave(around[i], within[i])) for i in range(2)]

    return dsp.env(dsp.mixstereo(together), dsp.randchoose(etypes))

out = dsp.mix([stream(i) for i in range(1,7)])

print dsp.write(out, 'haiku-12-02-25-gathering', False)
dsp.timer('stop')
