import dsp

dsp.timer('start')
dsp.seed('beed')

# Neat!

def bee(tonic, out=''):
    t = dsp.stf(20) / dsp.htf(tonic);
    s = dsp.wavetable('line', t)
    wtable = dsp.wavetable('sine2pi', dsp.htf(tonic))
    div = dsp.randint(100, 1000)

    for i in range(t):
        fp = (i % div) * 0.1 + 0.0001
        out += ''.join([dsp.pack(0.4 * f + (s[i] / (f + fp))) * 2 for f in wtable])

    return out

out = dsp.mix([bee(100 * i) for i in range(1, 10)], False)

print dsp.write(out, 'haiku-12-03-03-beed', False)
dsp.timer('stop')

