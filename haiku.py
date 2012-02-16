import fabric.fabric as dsp

dsp.timer('start') 
dsp.seed('crossing')

# Oh my god this is so much faster now.
# I'm just unpacking each frame on the fly to look for zero crossings instead 
# of building a lookup table and searching it. Seems ridiculous in retrospect
# that I thought that would be faster.
#
# Anyhow, this is pretty exciting - since this is pretty fast, it means that fabric 
# can begin to play in the frequency domain soon!

tonic = 300.0

ratios = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0, 6.0, 8.0]
pitches = [tonic * dsp.randchoose(ratios) + i for i in range(30)]
stack = [dsp.tone(dsp.stf(2), pitches[i] * dsp.randint(1, 4)) for i in range(30)]
stack = dsp.mix(stack)

stack = dsp.split(stack, 0, 2)
for i,c in enumerate(stack):
    c = dsp.list_split(c, 8)
    c = [ dsp.env(''.join(b) * dsp.randint(1,100), 'gauss') for b in c ]
    c = dsp.randshuffle(c)
    stack[i] = ''.join(c)

out = dsp.mixstereo(stack)

print dsp.write(out, 'haiku-12-02-16-crossing-second-variation', False)

dsp.timer('stop')
