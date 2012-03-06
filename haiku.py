import dsp

dsp.timer('start')
dsp.seed('Avian')

birds = dsp.read('sounds/nsong.wav')
birds = dsp.split(birds.data, dsp.stf(10)) * 2 
birds = birds[:12]

guitar = dsp.read('sounds/cguitar.wav')

def gcut(guitar, i, j=0):
    etypes = ['sine', 'line', 'phasor', 'tri']
    etypes += ['sine' for e in range(10)]

    t = dsp.stf(dsp.rand(20, 230))
    if t < dsp.stf(160):
        j = 20 * i
        if j % 3 == 0:
            guitar = dsp.amp(guitar, dsp.rand(1.0, 6.0))

    g = dsp.cut(guitar, dsp.stf((i + j) * 0.005 + 0.6), dsp.stf(i * 0.03 + 0.01))
    g = dsp.fill(g, t)
    g = dsp.split(g, dsp.flen(g) / dsp.randint(2, 32))
    g = [dsp.pan(s, dsp.rand()) for s in g]
    g = [dsp.env(s, dsp.randchoose(etypes)) for s in g]
    g = [dsp.amp(s, dsp.rand(0.05, 3.0)) for s in g]
    g = [dsp.pad(s, dsp.randint(0, t / 3), dsp.randint(0, t / 3)) for s in g]
    g = dsp.fill(''.join(g), t)

    return g

guitar = dsp.mix([gcut(guitar.data, i) for i in range(150)], False, 20.0)
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
