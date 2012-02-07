import fabric.fabric as dsp

dsp.timer('start') 

# This morning I am thinking about money.
# Insane thoughts don't collectively produce insane realities, 
# they produce insane behaviors, like money.

points = [['random', dsp.rand(700 + (i * dsp.rand(10, 80)), 20)] for i in range(20)]
sweeps = [dsp.breakpoint(points, 1000) for i in range(10)] 
sweeps = [[dsp.cycle(f) for f in freqs] for freqs in sweeps]
sweeps = [''.join(s) for s in sweeps]

out = dsp.mix(sweeps, False, 0.5)

print dsp.write(out, 'haiku', True)

dsp.timer('stop')
