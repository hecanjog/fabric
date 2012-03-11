import dsp

dsp.timer('start')
dsp.seed('drums')

guitar = dsp.read('sounds/hcj.samples.tones/tape220.wav')

scale = [1.0, 1.333, 1.5, 1.667, 2.0]
gamut = [s * octave * 0.5 for s in scale for octave in range(1, 5)] + [0.25]
gamut.sort()
gamut = [dsp.transpose(guitar.data, s) for s in gamut]
tonic = dsp.cut(gamut[0], 0, dsp.mstf(30 * 8))
snare = dsp.read('sounds/hcj.samples.hits/mix01.wav')
snare2 = dsp.read('sounds/hcj.samples.hits/snare.wav')
snare.data = dsp.amp(snare.data, 5.0)
snare2.data = dsp.amp(snare2.data, 1.0)
kick = dsp.read('sounds/hcj.samples.hits/idm2.wav')
kick.data = dsp.amp(kick.data, 3.0)

def ding(wlen, out=''):
    wave = [int(w * wlen) for w in dsp.wavetable('tri', wlen)]

    for i in range(150):
        h = dsp.cut(gamut[i * wave[i % len(wave)] % len(gamut)], dsp.mstf(dsp.rand(0, 1000)), dsp.mstf(30 * (i % 5)))
        h = dsp.pan(h, dsp.rand())
        h = dsp.env(h, 'phasor')
        h = dsp.amp(h, dsp.rand(0.2, 2.5))

        if i % 10 == 0:
            h = dsp.mix([h, dsp.fill(kick.data, dsp.flen(h))])

        if i % 7 == 0:
            h = dsp.mix([h, dsp.fill(snare.data, dsp.flen(h))])
        out += h

    numkicks = dsp.randint(8, 24)
    numsnares = dsp.randint(8, 16)

    kicklen = dsp.flen(out) / numkicks 
    snarelen = dsp.flen(out) / numsnares 

    k = dsp.pad(kick.data, 0, kicklen - dsp.flen(kick.data)) * numkicks 
    s = [dsp.cut(dsp.transpose(snare2.data, dsp.rand(0.98, 1.1)), 0, snarelen) for si in range(numsnares - 2)]
    s = dsp.pad('', snarelen, 0) + ''.join([dsp.pad(ss, 0, snarelen - dsp.flen(ss)) for ss in s])

    out = dsp.mix([out, k, s])

    return out

out = ''.join([dsp.transpose(dsp.pad(tonic, 0, dsp.mstf(30)), dsp.randint(0, 2) * 0.5 + 1) + ding(i) for i in range(1, 16)])

print dsp.write(out, 'haiku-12-03-11-drums', False)
dsp.timer('stop')
