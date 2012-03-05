import dsp

dsp.timer('start')
dsp.seed('avian')

birds = dsp.read('sounds/nsong.wav')
birds = dsp.split(birds.data, dsp.stf(10)) * 2 
birds = birds[:15]

guitar = dsp.read('sounds/cguitar.wav')

def gcut(guitar, i):
    g = dsp.cut(guitar, dsp.stf(i * 0.1 + 0.6), dsp.stf(i * 0.1 + 0.1))
    g = dsp.fill(g, dsp.stf(250))
    g = dsp.pan(g, dsp.rand())
    g = dsp.env(g, 'vary')

    return g

guitar = dsp.mix([gcut(guitar.data, i) for i in range(100)], True, 30.0)
guitar = dsp.split(guitar, dsp.flen(guitar) / 3)
guitar = dsp.env(guitar[0], 'line') + guitar[1] + dsp.env(guitar[2], 'phasor')

def sing(bird):
    bird = dsp.split(bird, dsp.mstf(dsp.randint(1, 200)))
    bird = [dsp.pan(b, dsp.rand()) for b in bird]
    bird = [dsp.env(b, 'random') for b in bird]
    bird = [dsp.amp(b, dsp.rand()) for b in bird]
    bird = ''.join(dsp.interleave(dsp.randshuffle(bird), bird))
    bird = dsp.env(bird, 'vary')

    return bird

birds = ''.join([sing(bird) for bird in birds])

out = dsp.mix([dsp.amp(birds, 0.5), dsp.pad(guitar, 0, dsp.stf(5))], False)

print dsp.write(out, 'haiku-12-03-05-avian', False)
dsp.timer('stop')
