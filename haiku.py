import dsp

dsp.timer('start')
dsp.seed('snow show')

# After Meg's birthday

fourth = 2**(5/12.0) - 1
scale = [2 - i * fourth for i in range(1, 6)]

def ring():
    arps = [dsp.mix([dsp.env(gamut[i % len(gamut)], 'sine'), dsp.env(dsp.randchoose(cgamut), 'sine')]) for i in range(75)]
    arps = [dsp.cut(a, dsp.randint(0, dsp.flen(a)), dsp.randint(4410, 44100 * 3)) for a in arps]
    arps = [dsp.pan(a, dsp.rand()) for a in arps]
    arps = [dsp.amp(a, dsp.rand()) for a in arps]
    arps = [dsp.fill(a, dsp.stf(20)) for a in arps]
    arps = [dsp.benv(a, [dsp.rand() for i in range(dsp.randint(5, 50))]) for a in arps]
    arps = dsp.mix(arps, True, 40.0)

    return arps

g = dsp.read('sounds/hcj.samples.tones/cyclohit.wav')
last = dsp.read('sounds/hcj.samples.tones/last.wav')
lastb = dsp.read('sounds/hcj.samples.tones/nick220.wav')

gamut = [dsp.transpose(last.data, s) for s in scale]
cgamut = [dsp.transpose(lastb.data, s) for s in scale]

out = g.data
out += ''.join([ring() for r in range(8)])

vc = dsp.read('sounds/violin-c.wav')
vd = dsp.read('sounds/violin-d.wav')
gamut = [dsp.transpose(vc.data, s) for s in scale]
cgamut = [dsp.transpose(vd.data, s) for s in scale]

out = dsp.mix([dsp.env(''.join([ring() for r in range(8)]), 'line'), out], False)
out += lastb.data

print dsp.write(out, 'haiku-12-03-14-snow-show', False)
dsp.timer('stop')
