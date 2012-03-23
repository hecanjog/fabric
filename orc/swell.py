import dsp
import wes

def play(args):
    freqs = [1,3,5]
    octave =3 
    pre = []
    length = dsp.stf(1)
    reps = 1
    volume = 1
    sounds = args.pop(0) 
    sounds = [sounds.va.data, sounds.vb.data, sounds.vc.data, sounds.vd.data, sounds.ve.data, sounds.vf.data, sounds.vg.data]
    violin = ''

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
            reps = int(a[1])

        if a[0] == 'p':
            prerender = True

        if a[0] == 'v':
            volume = float(a[1]) / 100.0

        if a[0] == 's':
            violin = sounds[ord(a[1]) - 97]

    freqs = [wes.scale[i - 1] * ( octave / 4.0 ) for i in freqs]

    dsp.dsp_grain *= 4
    line = wes.readline()

    for word in line: 
        vstart = int(wes.rword(word) * 44100)
        if violin == '':
            violin = sounds[int(wes.rword(word) * (len(sounds)-1))]
        v = dsp.cut(violin, vstart, length / len(line))
        v = dsp.mix([dsp.fill(dsp.transpose(v, f), length / len(line)) for f in freqs])
        v = dsp.env(v, 'sine', False, volume)

        v *= reps
            
        dsp.play(v)

    dsp.dsp_grain /= 4
