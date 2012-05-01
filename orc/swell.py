import dsp
import wes

def play(args):
    freqs = [1,8]
    octave = 4 
    pre = []
    length = dsp.stf(30)
    reps = 'n' 
    volume = 1
    pdevice = 'T6_pair1' 

    for arg in args:
        a = arg.split(':')
        if a[0] == 'f':
            freqs = a[1].split('.')
            freqs = [int(f) for f in freqs]

        if a[0] == 'o':
            octave = float(a[1])
            
        if a[0] == 't':
            length = dsp.stf(float(a[1]))

        if a[0] == 'r':
            reps = 'y' 

        if a[0] == 'v':
            volume = float(a[1]) / 100.0

        if a[0] == 's':
            violin = sounds[ord(a[1]) - 97]

        if a[0] == 'c':
            if int(a[1]) < len(dsp.io):
                if int(a[1]) > 0 and int(a[1]) <= len(dsp.io):
                    pdevice = dsp.io[int(a[1]) - 1]

    freqs = [wes.scale[i - 1] * ( octave / 4.0 ) for i in freqs]

    dsp.dsp_grain *= 4
    line = wes.readline()

    violin = dsp.rec(dsp.stf(2), dsp.io[0])

    for word in line: 
        if reps == 'y':
            violin = dsp.rec(dsp.stf(2), dsp.io[0])

        vstart = int(wes.rword(word) * 44100)
        v = dsp.mix([dsp.fill(dsp.env(dsp.cut(violin, vstart, dsp.mstf(wes.rword(word) * 1500 + 500)), 'sine'), length) for layer in range(10)])
        v = dsp.mix([dsp.fill(dsp.transpose(v, f), length) for f in freqs])
        v = dsp.env(v, 'sine', False, volume)
            
        dsp.play(v, pdevice)

    dsp.dsp_grain /= 4
