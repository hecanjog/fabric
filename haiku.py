import dsp

dsp.timer('start')
dsp.seed('empire builder')

# Pulse trains in Minnesota

def pulsetrain(numpulses):
    impulse = dsp.byte_string(32767) * 2 
    maxlength = dsp.randint(1000, 2000)

    lengths = dsp.wavetable('cos', numpulses)
    lengths = [int(i * maxlength) for i in lengths]
    pulses = [dsp.pan(impulse, dsp.rand()) for i in range(numpulses)]
    pulses = [dsp.pad(pulse, 0, lengths[i]) for i, pulse in enumerate(pulses)]

    pulses = ''.join(pulses)

    return pulses

out = dsp.mix([pulsetrain(10000) for i in range(10)], False)

print dsp.write(out, 'haiku-12-02-28-empire-builder', False)
dsp.timer('stop')
