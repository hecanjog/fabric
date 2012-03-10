import dsp
import time
import sys

scale = [1.0, 1.125, 1.25, 1.333, 1.5, 1.667, 1.875, 2.0]
freqs = [1,3,5]
octave_range = [4, 4]
pre = []
length = dsp.stf(3)
reps = 1
prerender = False

args = [arg for arg in sys.argv if arg != '']

for arg in args:
    a = arg.split(':')

    if a[0] == 'f':
        freqs = a[1].split('.')
        freqs = [int(f) for f in freqs]

    if a[0] == 'o':
        octave_range = a[1].split('.')
        octave_range = [float(o) for o in octave_range]
    
    if a[0] == 'l':
        length = dsp.stf(float(a[1]))

    if a[0] == 'r':
        reps = int(a[1])

    if a[0] == 'p':
        prerender = True


violin = dsp.read('sounds/violin-c.wav')
violin = [dsp.cut(violin.data, dsp.randint(0, 44100), length)]

freqs = [scale[i - 1] * ( dsp.rand(octave_range[0], octave_range[1]) / 4.0 ) for i in freqs]

dsp.dsp_grain *= 4

for i,v in enumerate(violin): 

    v = dsp.mix([dsp.fill(dsp.transpose(v, f), length) for f in freqs])
    v = dsp.env(v, 'sine')

    v *= reps
    
    if prerender == True:
        pre += [ dsp.cache(v) ]
    else:
        dsp.play(v)

dsp.dsp_grain /= 4
