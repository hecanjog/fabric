import dsp

dsp.timer('start')
dsp.seed('beec')

# Busy bees
# I revised this over 4+ hours, and ended up with
# almost nothing to show for it. So it goes!

def bee(tonic, out=''):
    t = dsp.stf(120) / dsp.htf(tonic);

    for i in range(t):
        wtable = dsp.wavetable('line', dsp.htf(tonic))
        out += dsp.pan(''.join([dsp.pack(0.4 * f * 2.0 - 1.0) * 2 for f in wtable]), dsp.rand())

    return out

out = dsp.mix([bee(100 * i) for i in range(1, 10)], False)

print dsp.write(out, 'haiku-12-03-02-beec', False)
dsp.timer('stop')

