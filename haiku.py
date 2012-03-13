import dsp

dsp.timer('start')
dsp.seed('bell arps')

# After Meg's birthday

arp = dsp.read('sounds/bellarp.wav')

fourth = 2**(5/12.0) - 1
scale = [2 - i * fourth for i in range(1, 6)]

gamut = [dsp.transpose(arp.data, s) for s in scale]

def ring():
    arps = [gamut[i % len(gamut)] for i in range(100)]
    arps = [dsp.cut(a, dsp.randint(0, dsp.flen(a)), dsp.randint(4410, 44100 * 3)) for a in arps]
    arps = [dsp.env(a, 'sine') for a in arps]
    arps = [dsp.pan(a, dsp.rand()) for a in arps]
    arps = [dsp.amp(a, dsp.rand()) for a in arps]
    arps = [dsp.fill(a, dsp.stf(75)) for a in arps]
    arps = [dsp.env(a, 'vary') for a in arps]
    arps = dsp.mix(arps)

    return arps

out = ''.join([ring() for r in range(8)])

print dsp.write(out, 'haiku-12-03-13-bell-arps', False)
dsp.timer('stop')
