import fabric.fabric as dsp

dsp.timer('start') 

sweeps = [dsp.wavetable('gauss', 1000, 700 + (i * 30), 20) for i in range(10)]
sweeps = [[dsp.cycle(f) for f in freqs] for freqs in sweeps]
sweeps = [''.join(s) for s in sweeps]

out = dsp.mix(sweeps, False, 0.5)

print dsp.write(out, 'haiku', True)

dsp.timer('stop')
