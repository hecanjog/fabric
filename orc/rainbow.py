import dsp
import wes

def play(args):
    sounds = args.pop(0)
    sounds = [sounds.va.data, sounds.vb.data, sounds.vc.data, sounds.vd.data, sounds.ve.data, sounds.vf.data, sounds.vg.data]
    length = dsp.stf(1)
    m = 20
    d = 3
    volume = 1.0
    violin = ''

    for arg in args:
        a = arg.split(':')

        if a[0] == 's':
            violin = sounds[ord(a[1]) - 97]

        if a[0] == 't':
            length = dsp.stf(float(a[1]))

        if a[0] == 'm':
            m = int(a[1])

        if a[0] == 'v':
            volume = float(a[1]) / 100.0

        if a[0] == 'd':
            d = float(a[1])


    elapsed = 0
    while elapsed < length:
        line = wes.readline()
        for word in line:
            if violin == '':
                violin = sounds[int(wes.rword(word) * (len(sounds)-1))]

            vstart = int(wes.rword(word) * (dsp.flen(violin) - (length / len(line))))
            v = dsp.cut(violin, vstart, length / len(line))

            numgrains = int(wes.rword(word) * m + len(word) + 2)
            grainampcurve = dsp.breakpoint([0] + [wes.rword(word) for gc in range(len(word))], numgrains)
            grainpancurve = dsp.breakpoint([0.5] + [wes.rword(word) for gc in range(len(word))], numgrains)
            grainpadcurve = dsp.breakpoint([wes.rword(word) * 200 for gc in range(len(word))], numgrains)
            grainlencurve = dsp.breakpoint([wes.rword(word) * 200 + 0.1 for gc in range(len(word))], numgrains)
            grainstartcurve = dsp.breakpoint([wes.rword(word) * (dsp.flen(v) - max(grainlencurve)) for gc in range(len(word))], numgrains)

            grains = []
            for i in range(numgrains):
                grainpan = grainpancurve[i] 
                grainamp = grainampcurve[i] * volume + 0.01
                grainenv = wes.wtypes[int(wes.rword(word) * (len(wes.wtypes)-1))]

                grain = dsp.cut(v, int(grainstartcurve[i]), int(grainlencurve[i]))
                grain = dsp.pan(grain, grainpan)
                grain = dsp.env(grain, grainenv, True, grainamp)
                grain = dsp.pad(grain, 0, int(grainpadcurve[i]))

                grains += [ grain ]

            wordpad = dsp.stf(wes.rword(word) * d)

            out = dsp.pad(''.join(grains), 0, wordpad)

            dsp.play(out)
       
            elapsed += dsp.flen(out)
