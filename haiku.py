import dsp
import wes

dsp.timer('start') 
dsp.seed('revember')

# Good enough for tonight.
#
# Violin: Meg Karls
# Poem: WC Tank
#
# Source sound here:
# http://sounds.hecanjog.com/violin-d.wav

poem = """
its cold everywhere here
i'm inventing a month called 'revember'
where there's reverb on every life sound
and you get to relive warmer
memories
"""

poem = wes.read(poem)
violin = dsp.read('sounds/violin-d.wav')

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
        shapes = ['line', 'phasor', 'sine', 'cos', 'flat']
        shapes += ['line' for pad in range(3)]

        for ie, element in enumerate(clang):
            # determine param based on char and 
            # process sound
            oindex = ord(chars[ie])
            print chars[ie], oindex

            if oindex < 91 and oindex > 64:
                speed = dsp.scale(0.05, 2.5, 64, 91, oindex)
                grainsize = (oindex - 64) * 2 + 10
            elif oindex < 123 and oindex > 96:
                speed = dsp.scale(0.05, 2.5, 96, 123, oindex)
                grainsize = (oindex - 96) * 2 + 10
            else:
                speed = 1.0
                grainsize = 40

            clang[ie] = wes.slow(element, speed, dsp.mstf(grainsize), 0, dsp.randchoose(shapes))

        clang = ''.join(clang)

        sequence[i] = dsp.pad(clang, 0, charlen * 2)
        print

    layers += [ ''.join(sequence) ]

out = dsp.mix([dsp.pan(l, i / float(len(layers) - 1)) for i,l in enumerate(layers)], False, 3.0)

print dsp.write(out, 'haiku-12-02-21-revember-second', False)

dsp.timer('stop') 
