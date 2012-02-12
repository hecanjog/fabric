import fabric.fabric as dsp
import math

dsp.timer('start') 
dsp.seed('multiples')

# It's John Cage day at the University of Iowa. I just heard 
# lecture on nothing and the sontas and interludes, and now there's 
# a music circus happening in the Iowa City mall. Brass!

def asound():
    material = dsp.randchoose(['tone','harmony','noise'])
    if material is 'tone':
        pitch = dsp.rand(20, 20000)
        length = dsp.randint(1, dsp.stf(10))
        silence = dsp.randint(0, dsp.stf(10))
        sound = dsp.tone(length, pitch, 'random', dsp.rand(0.001, 2.0))
        sound = dsp.env(sound, 'random', True)
        sound = dsp.pan(sound, dsp.rand())
        sound = dsp.pad(sound, silence / 2, silence / 2)
    elif material is 'harmony':
        pitches = [dsp.rand(20, 20000) for i in range(dsp.randint(1,10))]
        lengths = [dsp.randint(1, dsp.stf(10)) for i in pitches]
        silences = [dsp.randint(0, dsp.stf(10)) for i in pitches]
        sound = [dsp.tone(lengths[i], pitches[i], 'random', dsp.rand(0.001, 2.0)) for i in range(len(pitches))]
        sound = [dsp.env(dsp.pan(s, dsp.rand()), 'random', True) for s in sound]
        sound = [dsp.pad(s, silences[i] / 2, silences[i] / 2) for i,s in enumerate(sound)]
        sound = dsp.mix(sound)
    elif material is 'noise':
        length = dsp.rand(1, dsp.stf(10))
        amp = dsp.rand(0.001, 2.0)
        silence = dsp.randint(0, dsp.stf(10))
        sound = dsp.noise(length)
        sound = dsp.env(sound, 'random', True)
        sound = dsp.pan(sound, dsp.rand())
        sound = dsp.amp(sound, amp)
        sound = dsp.pad(sound, silence / 2, silence / 2)

    return sound

sounds = []
for i in range(dsp.randint(1,10)):
    sounds += [ ''.join([asound() for i in range(dsp.randint(1,10))]) ]

out = dsp.mix(sounds)

for i in range(dsp.randint(1,10)):
    sounds += [ ''.join([asound() for i in range(dsp.randint(1,10))]) ]

out += dsp.mix(sounds)

print dsp.write(out, 'haiku-12-02-12-multiples', False)

dsp.timer('stop')
