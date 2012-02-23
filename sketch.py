import dsp
import wes

dsp.timer('start') 
dsp.seed('revember')

# Just minor variations on yesterday's haiku today. 
# Uses an old song of mine as its source material.
#
# Poem: WC Tank
#
# Source sound here:
# http://sounds.hecanjog.com/june.wav

poem = """
its cold everywhere here
i'm inventing a month called 'revember'
where there's reverb on every life sound
and you get to relive warmer
memories
"""

poem = wes.read(poem)
violin = dsp.read('sounds/june.wav')

layers = []
for line in poem:
    linechars = wes.numchars(line)

    # collect segments of violin 
    # proportional to word lengths
    sequence = []
    start = 0
    for word in line:
        wordchars = len(word)

        wordproportion = 1.0 / (linechars / float(wordchars))
        seglen = int(dsp.flen(violin.data) * wordproportion)

        sequence += [ dsp.cut(violin.data, start, seglen) ]

        start += seglen

    # break word segments into characters and process
    for i, clang in enumerate(sequence):
        chars = list(line[i])
        charlen = dsp.flen(clang) / len(chars)
        clang = dsp.split(clang, charlen, 2)

        shapes =  ['phasor' for pad in range(2)]
        shapes += ['sine' for pad in range(2)]
        shapes += ['line' for pad in range(3)]
        shapes += ['vary' for pad in range(4)]
        shapes += ['impulse' for pad in range(4)]

        for ie, element in enumerate(clang):
            # determine param based on char and 
            # process sound
            oindex = ord(chars[ie])

            if oindex < 91 and oindex > 64:
                speed = dsp.scale(0.01, 3.0, 64, 91, oindex)
                grainsize = (oindex - 64) * 4 + 4 
            elif oindex < 123 and oindex > 96:
                speed = dsp.scale(0.01, 3.0, 96, 123, oindex)
                grainsize = (oindex - 96) * 4 + 4 
            else:
                speed = 1.0
                grainsize = 40

            print chars[ie], oindex, 's: ', speed, 'g: ', grainsize

            element = wes.slow(element, speed, dsp.mstf(grainsize), 0, dsp.randchoose(shapes))
            element = dsp.pan(element, dsp.rand())
            clang[ie] = dsp.env(element, dsp.randchoose(shapes))

        sequence[i] = ''.join(clang)
        print

    layers += [ ''.join(sequence) ]

out = dsp.mix(layers, False, 3.0)

print dsp.write(out, 'haiku-12-02-22-revember-third', False)

dsp.timer('stop') 
