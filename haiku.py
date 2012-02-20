import fabric.fabric as dsp

dsp.timer('start') 
dsp.seed('time')

# On the bus from Iowa City to Milwaukee
# 
# Violin performed by Meg Karls
# Source sound here:
# http://sounds.hecanjog.com/violin-c.wav

crush = dsp.read('sounds/violin-c.wav')
crush = dsp.split(crush.data, 0, 2)

mult = 16 

dsp.audio_params[0] = 1

for ci, chan in enumerate(crush):
    print ci, len(chan)
    lens = [dsp.flen(l) for l in chan]
    alen = int(sum(lens) / float(len(lens)))
    numwavelets = dsp.mstf(100) / alen

    print ci, alen, numwavelets

    chan = dsp.list_split(chan, numwavelets)

    for wi, wavelet in enumerate(chan):
        wavelet = ''.join(wavelet)
        wavelet = dsp.split(wavelet, dsp.flen(wavelet) / 2, 1)

        acap = dsp.cut(wavelet[0], 0, dsp.flen(wavelet[0]) / 2)
        acap = dsp.env(acap * 2, 'gauss', True)
        acap = dsp.cut(acap, dsp.flen(acap) / 2, dsp.flen(acap) / 2)

        bcap = dsp.cut(wavelet[1], dsp.flen(wavelet[1]) / 2, dsp.flen(wavelet[1]) / 2)
        bcap = dsp.env(bcap * 2, 'gauss', True)
        bcap = dsp.cut(bcap, 0, dsp.flen(bcap) / 2)
        
        wavelet[0], wavelet[1] = dsp.env(wavelet[0], 'gauss', True), dsp.env(wavelet[1], 'gauss', True)

        wmult = dsp.randint(2, mult * 2)

        lowerw = [ int(i % 2 == 0) for i in range(wmult - 1) ]
        upperw = [ i % 2 for i in range(wmult) ]

        wlower = acap + ''.join([wavelet[i] for i in upperw]) + bcap
        wupper = ''.join([wavelet[i] for i in lowerw])
        
        chan[wi] = dsp.mix([wlower, wupper])

    crush[ci] = ''.join(chan)

dsp.audio_params[0] = 2 
out = dsp.mixstereo(crush)

print dsp.write(out, 'haiku-12-02-19-time', True)

dsp.timer('stop') 
