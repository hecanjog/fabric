import fabric.fabric as dsp

dsp.timer('start') 
dsp.seed('Placements')
psize = 5777 

# A few hours in Milwaukee

etypes = ['line','sine','cos','impulse','sine2pi','cos2pi','saw','tri','flat']
points = [[dsp.randchoose(etypes), dsp.rand(977 + (i * dsp.rand(11, 77)), 77)] for i in range(psize)]
sweeps = [dsp.breakpoint(dsp.randshuffle(points), psize * 777) for i in range(7)] 
sweeps = [[dsp.cycle(f, 'tri') for f in freqs] for freqs in sweeps]
sweeps = [''.join(s) for s in sweeps]
sweeps = [dsp.pan(s, dsp.rand(0.0, 1.0)) for s in sweeps]

out = dsp.mix(sweeps, False, 0.5) # Right-aligned
out += dsp.mix(sweeps, True, 0.5) # Left-aligned

print dsp.write(out, 'haiku-12-02-08-placements', True)

dsp.timer('stop')
