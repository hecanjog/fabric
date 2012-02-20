import fabric.fabric as dsp

dsp.timer('start') 
dsp.seed('revember')

# On the bus from Milwaukee to Minnesota
#
# Mr Tank's poem is currently unused - tomorrow I'll try 
# mapping its structure to the granular process.
# 
# Violin: Meg Karls
# Poem: WC Tank
#
# Source sound here:
# http://sounds.hecanjog.com/violin-c.wav

poem = """
its cold everywhere here
i'm inventing a month called 'revember'
where there's reverb on every life sound
and you get to relive warmer
memories
"""

violin = dsp.read('sounds/violin-d.wav')

def slow(s, speed=0.5, grainsize=4410, out=''):
    inlen = dsp.flen(s)
    targetlen = int(inlen * (1.0 / speed))

    def bestfit(tlen, gsize, depth=0):
        if tlen % gsize != 0 and depth < 500:
            gsize = bestfit(tlen, gsize + 1, depth + 1)
        return gsize

    grainsize = bestfit(targetlen, grainsize)
    numgrains = targetlen / grainsize
    
    grains = []
    positions = dsp.wavetable('line', numgrains, inlen - grainsize, 0)
    for i in range(numgrains):
        grains += [dsp.cut(s, int(positions[i]), grainsize)]

    grains = [dsp.env(g, 'sine', True) for g in grains]
    grains = [''.join(grains), dsp.pad(''.join(grains[1:]), grainsize / 2, grainsize / 2)]

    out += dsp.mix(grains)

    return out

violin = dsp.split(violin.data, 4410, 2)
violins = [''.join([slow(v, dsp.rand(0.1, 2.0), dsp.mstf(dsp.randint(10, 120))) for v in violin]) for i in range(4)] 
out = dsp.mix(violins)

print dsp.write(out, 'haiku-12-02-20-revember', False)

dsp.timer('stop') 
