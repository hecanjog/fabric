import dsp
import sys
import sounds

args = [arg for arg in sys.argv if arg != '']

dsp.seed(args[1])

slen = dsp.mstf(dsp.randint(40, 1000))
violin = dsp.randchoose([sounds.va.data, sounds.vb.data, sounds.vc.data, sounds.vd.data, sounds.ve.data])
vlen = dsp.flen(violin)
violin = [dsp.cut(violin, dsp.randint(0, vlen - slen), slen) for i in range(len(args[1]))]
scale = [0.25, 0.5, 1.0, 1.667, 2.0, 3.0]

wtypes = ['sine', 'tri']

outs = []
for i,v in enumerate(violin): 
    v = dsp.transpose(v, dsp.randchoose(scale))
    v = dsp.benv(dsp.pan(v, dsp.rand()), [0] + [dsp.rand() for i in range(4)] + [0])
    v = dsp.pad(v, 0, dsp.randint(4410 * 2, 44100))
    #dsp.delay(dsp.rand(0.0, 0.2))
    
    outs += [ v ]

dsp.stream(outs)
