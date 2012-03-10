import dsp

dsp.timer('start')
dsp.seed('bell-variation')

guitar = dsp.read('sounds/hcj.samples.tones/tape220.wav')

scale = [1.333, 1.5, 1.667]
gamut = [s * octave * 0.5 for s in scale for octave in range(1, 3)] + [0.25]
gamut.sort()
gamut = [dsp.transpose(guitar.data, s) for s in gamut]
tonic = dsp.cut(gamut[0], 0, dsp.mstf(300))

def ding(wlen, out=''):
    wave = [int(w * wlen) for w in dsp.wavetable('tri', wlen)]

    for i in range(50):
        i = dsp.cut(gamut[i * wave[i % len(wave)] % len(gamut)], dsp.mstf(dsp.rand(0, 1000)), dsp.mstf(25 * (i % 5)))
        i = dsp.pan(i, dsp.rand())
        i = dsp.env(i, 'phasor')
        out += i

    return out

out = ''.join([tonic + ding(i) for i in range(1, 16)])

print dsp.write(out, 'haiku-12-03-10-bell-variation', False)
dsp.timer('stop')
