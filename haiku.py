import dsp

dsp.timer('start')
dsp.seed('pizza')

# Something of a drone

def pizza(freq, out=[]):
    frames = dsp.stf(60)
    pwtable = dsp.wavetable('line', frames)
    cwidth = dsp.htf(freq)

    print 'start pizza'

    def cook(f):
        plen = int(cwidth * 0.75 * pwtable[f])
        slen = cwidth - plen

        ptable = dsp.wavetable('phasor', plen)

        cpos = f % cwidth

        if cpos < plen:
            f = dsp.pack(ptable[cpos] - 0.5) * 2
        else:
            f = dsp.pack(0) * 2
            
        return f

    return ''.join([cook(f) for f in range(frames)])

out = dsp.mix([pizza(30 * i) for i in range(1, 7)])


print dsp.write(out, 'haiku-12-03-04-pizza', False)
dsp.timer('stop')

