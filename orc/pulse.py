import dsp
import wes

def play(args):
    t = dsp.stf(30)
    att = 10.0
    drift = 100000 
    volume = 1.0
    pdevice = 'T6_pair2'

    for arg in args:
        a = arg.split(':')

        if a[0] == 'a':
            att = float(a[1]) / 20.0

        if a[0] == 'd':
            drift = float(a[1]) * 1000

        if a[0] == 't':
            t = dsp.stf(float(a[1]))

        if a[0] == 'v':
            volume = float(a[1]) / 100.0

        if a[0] == 's':
            violin = sounds[ord(a[1]) - 97]

        if a[0] == 'c':
            if int(a[1]) < len(dsp.io):
                pdevice = dsp.io[int(a[1])]

    elapsed = 0
    line = wes.readline()
    w = 0
    violin = dsp.rec(dsp.stf(2), dsp.io[0])

    while elapsed < t:
        word = line[w % len(line)-1]

        divs = [int(wes.translate(a) * 7 + 1) for a in list(word)]

        streams = []
        for i,d in enumerate(divs):
            dlen = int((wes.rword(word) * 7 + 1) / d)
            v = dsp.cut(violin, dsp.mstf(wes.rword(word) * 1900), dsp.mstf(wes.rword(word) * 90 + 10))

            padtable = dsp.breakpoint([(wes.rword(word) + 0.5) * dlen * drift for bi in range(d / 4)], d)
            padtable = [int(bi) for bi in padtable]

            attacklen = int(dlen * wes.rword(word) * att) + 441
            silencelen = dlen - attacklen
            chord = dsp.fill(v, attacklen)
            chord = dsp.env(chord, 'phasor', volume)
            chord = dsp.pad(chord, 0, silencelen)
            chord = dsp.pan(chord, wes.rword(word))
            chord = ''.join([dsp.pad(chord, 0, padtable[dd]) for dd in range(d)])
            chord = dsp.benv(chord, [wes.rword(word) * volume for e in range(int(wes.rword(word) * 6) + 2)])
            streams += [ chord ]

        out = dsp.mix(streams)

        if dsp.flen(out) + elapsed > t:
            out = dsp.cut(out, 0, t - elapsed)

        dsp.play(out, pdevice)

        w += 1
        elapsed += dsp.flen(out)
