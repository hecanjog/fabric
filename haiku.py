import fabric.fabric as dsp
import audioop

dsp.timer('start') 
dsp.seed('crossing')

# I've been meaning to add a feature to Fabric to let me easily split a 
# sound by zero crossings. So! Here is a janky first test. Tomorrow I hope 
# to do some bug fixes and optimize, because janky does not begin to describe...
#
# I think the problem is that my zero crossings rarely nail zero exactly on the way from 
# negative to positive amplitudes. I should have guessed that!
#
# The function I wrote to test for crossings will have to be a little smarter
# and look for values within a certiain threshold - or even better, transitions 
# between positive and negative amplitudes.
#
# That will have to be for tomorrow, unless I find a little time to work on it tonight.
#
# In the meantime, I'm cheating and attenuating the input to create more obvious zeros.

tonic = 500.0

etypes = ['line', 'sine', 'cos', 'phasor', 'flat', 'gauss']
ratios = [0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0, 2.5, 3.0, 3.5, 4.0, 5.0, 6.0, 8.0]
pitches = [tonic * dsp.randchoose(ratios) + i for i in range(20)]
stack = [dsp.tone(dsp.stf(30), pitches[i]) for i in range(20)]
stack = [dsp.panenv(s, dsp.randchoose(etypes)) for s in stack]
stack = [dsp.env(s, dsp.randchoose(etypes)) for s in stack]
stack = dsp.mix(stack)
stack = dsp.amp(stack, 0.01)

def tomono(s):
    left = audioop.tomono(s, dsp.audio_params[1], 1, 0)
    right = audioop.tomono(s, dsp.audio_params[1], 0, 1)

    return [left, right] 

def stereomix(s):
    s[0] = audioop.tostereo(s[0], dsp.audio_params[1], 1, 0)
    s[1] = audioop.tostereo(s[1], dsp.audio_params[1], 0, 1)
    return dsp.mix(s) 

def getchunks(s):
    # the brute force approach...
    all = dsp.split(s, 1)
    chunk, chunks = [], []
    zero = dsp.byte_string(0) * dsp.audio_params[1]

    for frame in all:
        if chunk == []:
            chunk += [ frame ]
        elif frame != zero and chunk != []:
            chunk += [ frame ]
        elif frame == zero and chunk != []:
            chunk += [ frame ]
            chunks += [ ''.join(chunk) ]
            chunk = []

    print len(chunks)

    return chunks

def shufflecrossings(s):
    chans = tomono(s)
    chans = [getchunks(c) for c in chans]
    chans = [dsp.randshuffle(c) for c in chans]
    chans = [''.join(c) for c in chans]

    return stereomix(chans)

out = dsp.amp(shufflecrossings(stack), 20)

print dsp.write(out, 'haiku-12-02-14-crossing', False)

dsp.timer('stop')
