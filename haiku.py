import fabric.fabric as dsp
import struct

dsp.timer('start') 

# This is my submission for the 7th disquiet junto project.
#
# The script breaks the sound by zero crossings in each channel, 
# then reads through each sample in the packet and converts it into 
# an integer. The integer is then converted into a literal string 
# and if the ordinal index of any character in the string is divisible 
# by 5, it replaces that character with a zero. Then, the string is 
# converted back to an integer, packed back into wave data, and mixed 
# back into a stereo sound.
#
# The result ended up translating the crashing waves into a kind of 
# soft rolling crackle. I was expecting to have to try several iterations 
# of different replace-with-zero schemes before landing on something that 
# sounded nice. Got lucky on the first try, though!
#
# The source audio for this composition is a recording by Luftrum of 
# waves crashing on the shore of Kalundborg Fjord at Røsnæs, Denmark:
#
# http://www.freesound.org/people/Luftrum/sounds/48412 
#
# More details on the Disquiet Junto at:
# http://soundcloud.com/groups/disquiet-junto

crush = dsp.read('sounds/crushing.wav')
crush = dsp.split(crush.data, 0, 2)

for ci, chan in enumerate(crush):
    for wi, wavelet in enumerate(chan):
        # I thought maybe I would do something special
        # at the wavelet level, but I didn't feel it needed more.

        frames = dsp.split(wavelet, 1, 1)
        
        for fi, frame in enumerate(frames):
            fint = struct.unpack("<h", frame)

            fint = str(fint[0])
            fint = list(fint)
            
            for fifi, fc in enumerate(fint):
                if ord(fc) % 5:
                    fint[fifi] = "0"

            fint = ''.join(fint)
            fint = int(fint)
            frames[fi] = dsp.byte_string(fint)

        chan[wi] = ''.join(frames)

    crush[ci] = ''.join(chan)

out = dsp.mixstereo(crush)

print dsp.write(out, 'haiku-12-02-17-crushing', False)

dsp.timer('stop')
