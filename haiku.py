import dsp

dsp.timer('start')
dsp.seed('destroy empire')

# Ray guns! Spaceship engines! Hints of the THX sound!
#
# Not sure how that happened.

def pulsetrain(numpulses):
    impulse = dsp.byte_string(32767) * 2 
    maxlength = dsp.randint(10, 300)

    points = [0.0] + [['line', dsp.rand()] for i in range(30)]
    lengths = dsp.breakpoint(points, numpulses)
    lengths = [int(i * maxlength) for i in lengths]
    pulses = [dsp.pan(impulse, dsp.rand()) for i in range(numpulses)]
    pulses = [dsp.pad(pulse, 0, lengths[i]) for i, pulse in enumerate(pulses)]

    pulses = ''.join(pulses)

    return pulses

out = dsp.mix([pulsetrain(20000) for i in range(100)], False, 10.0)

print dsp.write(out, 'haiku-12-02-29-destroy-empire', False)
dsp.timer('stop')
