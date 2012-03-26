
def slow(s, speed=0.5, grainsize=4410, transpose=0, shape='line', out=''):
    inlen = dsp.flen(s)
    targetlen = int(inlen * (1.0 / speed))

    def bestfit(tlen, gsize, depth=0):
        if tlen % gsize != 0 and depth < 500:
            gsize = bestfit(tlen, gsize + 1, depth + 1)
        return gsize

    grainsize = bestfit(targetlen, grainsize)
    numgrains = targetlen / grainsize
    
    grains = []
    positions = dsp.wavetable(shape, numgrains, inlen - grainsize, 0)
    for i in range(numgrains):
        grains += [dsp.cut(s, int(positions[i]), grainsize)]

    if transpose > 0:
        grains = [dsp.transpose(g, transpose) for g in grains]
        grains = [dsp.fill(g, grainsize) for g in grains]

    grains = [dsp.env(g, 'sine', True) for g in grains]
    grains = [''.join(grains), dsp.pad(''.join(grains[1:]), grainsize / 2, grainsize / 2)]

    out += dsp.mix(grains)

    return out


