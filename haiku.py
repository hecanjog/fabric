import dsp

dsp.timer('start')
dsp.seed('drum variation')

guitar = dsp.read('sounds/bellarp.wav')

scale = [1.0, 1.5, 2.0, 3.0]
gamut = [s * octave * 0.25 for s in scale for octave in range(1, 3)] + [0.25]
gamut.sort()
gamut = [dsp.transpose(guitar.data, s) for s in gamut]
tonic = dsp.cut(gamut[0], 0, dsp.mstf(30 * 8))

def ding(wlen, beat, out=''):
    wave = [int(w * wlen) for w in dsp.wavetable('line', wlen)]
    k = dsp.randchoose(gamut)
    s = dsp.randchoose(gamut)

    for i in range(150):
        h = dsp.cut(gamut[i * wave[i % len(wave)] % len(gamut)], dsp.stf(dsp.rand(0, 4)), dsp.mstf(beat * (i % 5)))
        h = dsp.pan(h, dsp.rand())
        h = dsp.env(h, 'random')
        h = dsp.amp(h, dsp.rand(0.2, 2.5))

        out += h

    numkicks = dsp.randint(4, 36)
    numsnares = numkicks / dsp.randint(2, 5) 

    kicklen = dsp.flen(out) / numkicks 
    snarelen = dsp.flen(out) / numsnares 

    k = dsp.pad(dsp.env(dsp.fill(k, kicklen), 'random'), 0, kicklen - dsp.flen(k)) * numkicks 
    s = dsp.pad(dsp.env(dsp.fill(s, snarelen), 'random'), 0, snarelen - dsp.flen(s)) * numsnares 

    out = dsp.mix([out, dsp.fill(k, dsp.flen(out)), dsp.fill(s, dsp.flen(out))])

    return out

beats = [25, 50, 75, 100]
out = ''.join([dsp.transpose(dsp.pad(tonic, 0, dsp.mstf(30)), dsp.randint(0, 2) * 0.5 + 1) + ding(i, dsp.randchoose(beats)) for i in range(1, 16)])

print dsp.write(out, 'haiku-12-03-12-drums-variation', False)
dsp.timer('stop')
