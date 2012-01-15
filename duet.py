#!/usr/bin/env python2
# -*- coding: UTF-8 -*-

import fabric.fabric as dsp

def main(out=''):
    dsp.timer('start') 
    dsp.snddir = 'sounds/'
    dsp.seed('disquiet0002-duet')

    orc = Orc()

    tonic = 250.0

    layers = []
    layers.append(orc.scrub([tonic + dsp.rand(-1.0, 1.0)], dsp.stf(245), 'sine', (0.1, dsp.mstf(2000))))
    layers.append(orc.scrub([tonic * 2 + dsp.rand(-1.0, 1.0) ], dsp.stf(230), 'sine', (0.11, dsp.mstf(2000))))
    layers.append(orc.scrub([tonic * 3 + dsp.rand(-1.0, 1.0) ], dsp.stf(215), 'sine', (0.12, dsp.mstf(2000))))
    
    layers.append(orc.scrub([tonic * 1.5 * i + dsp.rand(-1.0, 1.0) for i in range(1, 3)], dsp.stf(200), 'sine', (0.3, dsp.mstf(1500))))

    layers.append(orc.scrub([tonic * 1.25 * i + dsp.rand(-1.0, 1.0) for i in range(1, 3)], dsp.stf(130), 'phasor', (0.2, dsp.mstf(1500))))
    layers.append(orc.scrub([tonic * 2.25 * i + dsp.rand(-1.0, 1.0) for i in range(1, 2)], dsp.stf(140), 'sine', (0.4, dsp.mstf(2000))))
    layers.append(orc.scrub([tonic * 2.25 * i + dsp.rand(-1.0, 1.0) for i in range(1, 2)], dsp.stf(140), 'sine', (0.5, dsp.mstf(1000))))

    layers = [dsp.env(layer, 'sine') for layer in layers]

    asun = orc.scrub([tonic * 4], dsp.stf(3), 'sine', (0.32, dsp.mstf(500)))
    bsun = orc.scrub([tonic * 3], dsp.stf(3), 'sine', (0.3, dsp.mstf(500)))

    out += dsp.mix([dsp.mix(layers, False), dsp.env(orc.burstsun(bsun, 550), 'phasor'), dsp.env(orc.burstsun(asun, 600), 'phasor')])

    out = dsp.write(out, 'duet', True)
    dsp.timer('stop')

class Orc:
    """ Do things, play things """

    def __init__(self):
        self.horn = dsp.read('horn.wav')

    def burstsun(self, snd, numtimes, out=''):
        horns = [dsp.cut(snd, i * dsp.mstf(4), 2**i) for i in range(numtimes)]
        horns = [dsp.panenv(h, 'random', 'sine', dsp.rand() * 0.5, dsp.rand() * 0.5 + 0.5) for h in horns]

        out += ''.join(horns)

        return out

    def scrub(self, pitches, length, wtype, sel=(0.0, 44100), out=''):
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
            layers.append(''.join([dsp.env(dsp.cut(self.horn.data, int(i), dsp.htf(pitch)), 'sine') for i in wtable]))

        out += dsp.mix(layers, True, 2.0)

        return out 
      
if __name__ == '__main__':
    main()
