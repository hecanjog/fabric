#!/usr/bin/env python2
# -*- coding: UTF-8 -*-

import fabric.fabric as dsp

def main(out=''):
    dsp.timer('start') 
    dsp.snddir = 'sounds/'
    dsp.seed('duet')

    orc = Orc()

    tonic = 250.0
    llen = dsp.stf(1200)
    layers = []

    # Opening high tones
    hi = orc.scrub([tonic * 12, tonic * 3, tonic * 6], int(llen * 0.25), 'random', (0.0, dsp.mstf(100)))
    hi = dsp.split(hi, int(llen * 0.0125))
    hi = [dsp.env(h, 'sine') for h in hi]
    layers.append(dsp.pad(dsp.mix([''.join(hi), orc.scrub([tonic * 6, tonic * 3], int(llen * 0.25), 'sine', (0.0, dsp.mstf(2000)), 'random')]), 0, int(llen * 0.74)))

    # Opening tones P1, P8, P12
    layers.append(orc.scrub([tonic + dsp.rand(-1.0, 1.0)], int(llen * 1.0), 'sine', (0.3, dsp.mstf(2000))))
    layers.append(orc.scrub([tonic * 2 + dsp.rand(-1.0, 1.0) ], int(llen * 0.95), 'sine', (0.33, dsp.mstf(4000))))
    layers.append(orc.scrub([tonic * 3 + dsp.rand(-1.0, 1.0) ], int(llen * 0.97), 'sine', (0.32, dsp.mstf(2000))))

    layers = [dsp.env(layer, 'sine') for layer in layers]
    layers[0] = dsp.mix(layers, False, 4.0) # Preventing out of memory errors
   
    # Middle tones, rougher P5, P8
    layers.append(orc.scrub([tonic * 1.5 * i + dsp.rand(-1.0, 1.0) for i in range(1, 3)], int(llen * 0.7), 'sine', (0.3, dsp.mstf(5500))))
    layers.append(orc.scrub([tonic * 2 * i + dsp.rand(-1.0, 1.0) for i in range(1, 2)], int(llen * 0.7), 'sine', (0.35, dsp.mstf(6500)), 'gauss'))
    layers.append(orc.scrub([tonic * 2 * i + dsp.rand(-1.0, 1.0) for i in range(1, 2)], int(llen * 0.75), 'sine', (0.4, dsp.mstf(4500)), 'phasor'))

    layers[0] = dsp.mix(layers, False, 4.0)

    # End tones, M3, M9
    layers.append(orc.scrub([tonic * 1.25 * i + dsp.rand(-1.0, 1.0) for i in range(1, 3)], int(llen * 0.45), 'phasor', (0.2, dsp.mstf(4500))))
    layers.append(orc.scrub([tonic * 2.25 * i + dsp.rand(-1.0, 1.0) for i in range(1, 2)], int(llen * 0.55), 'sine', (0.4, dsp.mstf(4000))))
    layers.append(orc.scrub([tonic * 2.25 * i + dsp.rand(-1.0, 1.0) for i in range(1, 2)], int(llen * 0.5), 'sine', (0.5, dsp.mstf(5000)), 'random'))

    layers[0] = dsp.mix(layers, False, 4.0)

    # Coda tones, low tonics
    layers.append(orc.scrub([tonic * 0.25, tonic * 0.125], int(llen * 0.2), 'line', (0.35, dsp.mstf(2500))))
    layers.append(orc.scrub([tonic * 0.25, tonic * 0.5], int(llen * 0.2), 'line', (0.37, dsp.mstf(1500)), 'random'))

    thesun = orc.scrub([tonic * 50, tonic, tonic * 49, tonic * 48, tonic * 24 ], dsp.stf(10), 'sine', (0.32, dsp.mstf(3000)), 'random')
    suns = dsp.mix([orc.burstsun(dsp.amp(thesun, 0.9), int(llen * 1.0)) for i in range(6)])

    out += dsp.env(dsp.mix([dsp.mix(layers, False, 4.0), suns], False), 'sine')

    out = dsp.write(out, 'duet', True)
    dsp.timer('stop')

class Orc:
    """ Do things, play things """

    def __init__(self):
        self.horn = dsp.read('horn.wav')

    def burstsun(self, snd, length, out=''):
        numtimes = int(length / dsp.mstf(1000))
        ptable = dsp.wavetable('sine', numtimes, dsp.flen(snd) - dsp.mstf(100), 0)
        ltable = dsp.breakpoint([['random', dsp.randint(dsp.mstf(80), dsp.mstf(1000))] for i in range(numtimes / 40)], numtimes)
        horns = [dsp.pad(dsp.env(dsp.cut(snd, int(ptable[i]), int(ltable[i])), 'sine', True), 0, dsp.randint(int(i * 0.05), int(i * 0.5))) for i in range(numtimes)]

        out += dsp.fill(dsp.pulsar(''.join(horns)), length)

        return out

    def scrub(self, pitches, length, wtype, sel=(0.0, 44100), gtype='sine', out=''):
        layers = []

        for pitch in pitches:
            numcycles = length / dsp.htf(pitch)

            if sel[0] == 'rand':
                fstart = dsp.rand() * dsp.flen(self.horn.data) - dsp.htf(pitch)
            else:
                fstart = sel[0] * dsp.flen(self.horn.data) - dsp.htf(pitch)

            fend = fstart + sel[1]

            if length % dsp.htf(pitch) > 0:
                numcycles += 1

            wtable = dsp.wavetable(wtype, numcycles, fend, fstart)
            layers.append(''.join([dsp.env(dsp.cut(self.horn.data, int(i), dsp.htf(pitch)), gtype) for i in wtable]))

        out += dsp.mix(layers, True, 2.0)

        return out 
      
if __name__ == '__main__':
    main()
