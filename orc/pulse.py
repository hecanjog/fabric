import dsp
import wes

def play(args):
    sounds = args.pop(0)

    t = dsp.stf(10)
    m = 3 
    volume = 1.0
    sounds = [sounds.va.data, sounds.vb.data, sounds.vc.data, sounds.vd.data, sounds.ve.data, sounds.vf.data, sounds.vg.data]
    violin = ''

    for arg in args:
        a = arg.split(':')

        if a[0] == 't':
            t = dsp.stf(float(a[1]))

        if a[0] == 'm':
            m = int(a[1])

        if a[0] == 'v':
            volume = float(a[1]) / 100.0

        if a[0] == 's':
            violin = sounds[ord(a[1]) - 97]


    elapsed = 0
    line = wes.readline()
    w = 0

    while elapsed < t:
        word = line[w % len(line)-1]
        if violin == '':
            violin = sounds[int(wes.rword(word) * (len(sounds)-1))]

        fraglen = dsp.mstf(wes.rword(word) * 1000 + 30)
        seglen = len(word) * fraglen

        divs = [int(wes.translate(a) * 7 + 1) for a in list(word)]

        chordsize = int(wes.rword(word) * 5 + 2)

        chords = []
        for i in range(chordsize):
            chord = [dsp.cut(violin, int(wes.rword(word) * (dsp.flen(violin) - seglen)), seglen) for j in range(len(divs))]
            chords += [ dsp.mix(chord, False, wes.rword(word) * 30 + 3) ]

        streams = []
        for i,d in enumerate(divs):
            i = i % len(chords)-1
            dlen = seglen / d

            padtable = dsp.breakpoint([wes.rword(word) * dlen * 0.125 for bi in range(d / 4)], d)
            padtable = [int(bi) for bi in padtable]

            attacklen = int(dlen * wes.rword(word) * 0.5) + 41
            silencelen = dlen - attacklen
            chord = dsp.fill(chords[i], attacklen)
            chord = dsp.env(chord, 'phasor', volume)
            chord = dsp.pad(chord, 0, silencelen)
            chord = dsp.pan(chord, wes.rword(word))
            chord = ''.join([dsp.pad(chord, 0, padtable[dd]) for dd in range(d)])
            chord = dsp.benv(chord, [wes.rword(word) * volume for e in range(int(wes.rword(word) * 7) + 2)])
            streams += [ chord ]

        out = dsp.mix(streams) * len(word) * m

        if dsp.flen(out) + elapsed > t:
            out = dsp.cut(out, 0, t - elapsed)

        dsp.play(out)
        w += 1
        elapsed += dsp.flen(out)
