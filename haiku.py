import fabric.fabric as dsp
import struct

dsp.timer('start') 
dsp.seed('william')

# A variation on my haiku from yesterday, this time on 
# a short violin recording from a section of a violin and 
# computer piece I did with Meg Karls last year. 

crush = dsp.read('sounds/violin-d.wav')
crush = dsp.split(crush.data, 0, 2)
r = [1.0, 1.5, 2.0]

dsp.audio_params[0] = 1

for ci, chan in enumerate(crush):
    for wi, wavelet in enumerate(chan):
        if dsp.randint(0, 10) % 3 > 0:
            wavelet = wavelet * dsp.randint(2, 8)
            harm = [dsp.transpose(wavelet, dsp.randchoose(r)) for i in range(3)]
            harm = [dsp.fill(h, dsp.flen(wavelet)) for h in harm]
            chan[wi] = dsp.mix(harm)

        frames = dsp.split(wavelet, 1, 1)

        if dsp.randint(0, 10) % 3 > 0:
        
            for fi, frame in enumerate(frames):
                fint = struct.unpack("<h", frame)

                fint = str(fint[0])
                fint = list(fint)
            
                for fifi, fc in enumerate(fint):
                    if ord(fc) % 5 > 0:
                        fint[fifi] = "0"

                fint = ''.join(fint)
                fint = int(fint)
                frames[fi] = dsp.byte_string(fint)

            chan[wi] = ''.join(frames)

    crush[ci] = ''.join(chan)

dsp.audio_params[0] = 2 
out = dsp.mixstereo(crush)

print dsp.write(out, 'haiku-12-02-18-william', False)

dsp.timer('stop')
