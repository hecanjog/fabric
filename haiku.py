import fabric.fabric as dsp
import audioop

dsp.timer('start') 
dsp.seed('crossing')

# Part two in the land of zero crossings!
#
# Previously, I'd taken this script far enough to stupidly look for 
# boundries broken by literal zeros, but didn't consider that in almost 
# all cases the signal leaps right over zero on its way from positive to negative 
# values and back. If you're following along at home, this is because digital sound is 
# discrete - which means that in a given time frame there are only so many values 
# that can be crammed into the representation of the sound, depending on the samplng rate 
# and bit depth you're working at.
#
# Fabric is currently locked to cramming 44,100 samples into every second, with each sample 
# representing a number between -32,768 and 32,767. That means signals often do things like this:
#
#  1 *.             .*.
#      '.         .'   '.
#  0 ----'.-----.'-------'.
#          '. .'
# -1         *
#              
# In the above goofy ASCII diagram, look at how the dots don't nail the zero line exactly. 
# Imagine that the pixels on the Y axis represent all 16 bits of amplitude, with 0 to 32,767 above
# and -32,768 to 0 below. Then the X axis represents each sample in time - at a resolution of 44,100 
# of samples every second. My stupid waveform leaps over the zero on every crossing, because the resolution 
# in both directions isn't fine enough to represent it exactly.
#
# Okay, so here's my plan. It seems like it will be more expensive (read: slow) to actually convert every 
# sample from bytes to integers to look for transitions than it will be to make a list of all possible integers 
# as bytes and do a comparison. That's just a hunch, but my theory is comparing two strings is faster than encoding 
# and decoding integers as properly formatted bytes of data. (That's how fabric operates on sound: as lists of strings 
# of bytes - which also means it will happily shuffle samples around having no regard for their value.)
#
# [ Implements the idea above ]
#
# Gosh, I didn't account for the overhead that searching a giant list of items creates. It's very slow to search though 
# more than 65,000 values to find a match for each sample in each channel of a sound. Duh! I didn't consider that.
# This may lead to another variation tomorrow with a more direct approach using struct to translate the entire sample 
# first - probably then stored as a dict with amplitude keys? I might just add this to fabric core and do something 
# more musical with tomorrow's haiku, too... :-)
#
# For now, it works - though very slowly and probably bug infestedly...
#
# Outside of the janky zero crossing detection, the script doesn't do much:
#
# It mixes 30 1 second sinewaves, splits the stereo mix into left and 
# right channels, and breaks each channel into a list of segments divided at zero 
# crossings. Then it copies each segment between 2**0 and 2**10 times, attenuates that 
# segment by between 30 and 100% of the original amplitude, and then mixes the results 
# back into a stereo sound.

tonic = 500.0

ratios = [0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0, 2.5, 3.0, 3.5, 4.0, 5.0, 6.0, 8.0]
pitches = [tonic * dsp.randchoose(ratios) + i for i in range(30)]
stack = [dsp.tone(dsp.stf(1), pitches[i]) for i in range(30)]
stack = dsp.mix(stack)

gamut = [dsp.byte_string(i) for i in range(-32768, 32768)]

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
    all = dsp.split(s, 1, 1)
    chunk, chunks = [], []

    for i, frame in enumerate(all):
        try:
            if chunk == []:
                chunk += [ frame ]
            elif detectcrossing(frame, all[i+1]) == False and chunk != []:
                chunk += [ frame ]
            elif detectcrossing(frame, all[i+1]) == True and chunk != []:
                chunk += [ frame ]
                chunks += [ ''.join(chunk) ]
                chunk = []
        except IndexError:
            chunk += [ frame ]

    print len(chunks)

    return chunks

def detectcrossing(first, second):
    global gamut

    try:
        firstpos = gamut.index(first)
        secondpos = gamut.index(second)
    except ValueError:
        import struct
        print "Not found! Did you turn it up to 11?"
        print struct.unpack("<h", first), struct.unpack("<h", second)
        return False

    if firstpos > 32767:
        if secondpos < 32768:
            return True
    elif firstpos < 32768:
        if secondpos > 32767:
            return True

    return False

def shufflecrossings(s):
    chans = tomono(s)
    chans = [getchunks(c) for c in chans]
    chans = [''.join([dsp.amp(b * 2 ** dsp.randint(0,10), dsp.rand(0.3, 1.0)) for b in c]) for c in chans]

    return stereomix(chans)

out = shufflecrossings(stack)

print dsp.write(out, 'haiku-12-02-15-crossing-variation', False)

dsp.timer('stop')
