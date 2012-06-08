import dsp
import math

def pop(u, out=''):
    x = dsp.rand(0.1, 0.5) 
    m = dsp.rand(0.03, 5.5) 
    r = dsp.rand(3.765, 3.8)
    l = dsp.randint(10, u) 

    for t in range(l):
        b = ''
        x = r * x * (1.0 - x)
        s = int(math.fabs(x) * x * 100 + 4)

        for i in range(s):
            b += dsp.pad(dsp.pack(i / float(s)) * 2, 0, int(s * 0.5 + (i * m)))

        print x
        out += dsp.pan(b, x)

    return out

out  = dsp.mix([pop(50) for p in range(2)], True, 1)
out += dsp.mix([pop(10) for p in range(10)], True, 30)
out += dsp.mix([pop(20) for p in range(10)], True, 30)
out += dsp.mix([pop(300) for p in range(3)], True, 2)

dsp.write(out, 'pop')
