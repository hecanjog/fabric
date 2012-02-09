import fabric.fabric as dsp
import math

dsp.timer('start') 
dsp.seed('silent')
psize = 99 

# I forgot my headphones and I'm in a library, so who knows what this sounds like?

etypes = ['line','sine','cos','impulse','sine2pi','cos2pi','saw','tri','flat']

def brown(size):
    browns = dsp.wavetable('sine', size)
    browns = [ math.fabs(b + (dsp.rand(-0.02,0.02)) * dsp.rand(1.0,1.1)) for b in browns ]
    return browns

browns = brown(psize)
points = [[dsp.randchoose(etypes), browns[i]] for i in range(psize)]

sweeps = [dsp.breakpoint(points, psize * 99) for i in range(9)] 
sweeps = [[dsp.cycle(f * 1000 + 80, 'tri') for f in freqs] for freqs in sweeps]
sweeps = [''.join(s) for s in sweeps]
sweeps = [dsp.pan(s, dsp.rand(0.0, 1.0)) for s in sweeps]

out = dsp.mix(sweeps, False, 0.5) # Right-aligned
out += dsp.mix(sweeps, True, 0.5) # Left-aligned

print dsp.write(out, 'haiku-12-02-09-silent', False)

dsp.timer('stop')
