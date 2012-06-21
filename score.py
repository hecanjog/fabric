import dsp

"""
This is an example score with a very simple format.
It demonstrates some basic features in Fabric.

It generates ten 10 second long sinewaves at each 
integer harmonic starting from 330hz, then it 
applies an amplitude envelope to each sinewave by 
selecting the type of envelope randomly from the list
we chose, pans each sinewave to a random position across 
the stereo field, and then mixes them all together and 
outputs the result as a wave file.

I find it less confusing to refer to digital samples as 
frames, so you'll see that here. When I write frame, I 
mean a single mono sample with a width of two bytes, or a 
single stereo sample with a total width of four bytes. 

It's best to think in frames when dealing with fabric rather 
than string lengths, since those will vary depending on the 
number of channels being dealt with. To get the length in frames
of a sound, use the dsp.flen() function rather than Python's 
built in len() function, unless you prefer to make the translations
yourself!

"""

# dsp.seed accepts any string as input to be used as a seed for 
# fabric's internal pseudo-random functions. These functions don't 
# make any attempt to be as random as random can be, but each call 
# to fabric's internal random functions is derived from this initial 
# seed, so you can render this file 1000 times and it will always 
# produce the same result. If you'd like to fallback to python's 
# internal random module, just don't set a seed value, and the 
# random functions will generate new values on every render.
dsp.seed('fabric')

# Start timing the render. This has nothing 
# to do with audio timing, it's just a handy 
# way to know how long a render took to complete.
dsp.timer('start')

# there are more wavetypes available, but we'll just use some simple ones here.
wavetypes =  ['sine', 'line']
wavetypes += ['phasor' for i in range(3)] # Pad the random choice with 3 phasors

# Tone's arguments are the length to generate in frames, the frequency, 
# the waveshape, and the amplitude.
sinewaves = [dsp.tone(dsp.stf(10), 330 * i, 'sine2pi', 0.3) for i in range(1, 11)]

# dsp.env's arguments are the sound to be enveloped (a string of bytes) and the type 
# of envelope to apply. A boolean may be passed optionally as a third argument to 
# force the envelope to calculate at a resolution of a single sample - this is False 
# by default. It applies the amplitude changes to create the envelope in blocks of 
# 64 frames by default.
sinewaves = [dsp.env(sinewave, dsp.randchoose(wavetypes)) for sinewave in sinewaves]

# dsp.pan's arguments are the sound to be panned, and a number between 0 and 1
# to indicate pan position, where 0 is 100% left and 1 is 100% right.
sinewaves = [dsp.pan(sinewave, dsp.rand(0.0, 1.0)) for sinewave in sinewaves]

# Mix the sinewaves together. dsp.mix accepts a list of sounds to mix, and 
# defaults to left-aligning them if they are different lengths, the second 
# argument is a boolean which can be set to False to right-align sounds.
out = dsp.mix(sinewaves)

# The dsp.write function returns the rendered filename, so we print that here
print dsp.write(out, 'render', True)

# Stops the timer and prints the render time
dsp.timer('stop')
