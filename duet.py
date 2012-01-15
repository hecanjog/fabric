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
    layers.append(orc.scrub([tonic * i + dsp.rand(-1.0, 1.0) for i in range(1, 3)], dsp.stf(260), 'sine', (0.0, dsp.mstf(2500))))
    layers.append(orc.scrub([tonic * 1.25 * i + dsp.rand(-1.0, 1.0) for i in range(1, 3)], dsp.stf(260), 'phasor', (0.5, dsp.mstf(2500))))
    layers.append(orc.scrub([tonic * 1.5 * i + dsp.rand(-1.0, 1.0) for i in range(1, 3)], dsp.stf(260), 'sine', (0.1, dsp.mstf(2500))))

    layers.append(orc.scrub([tonic * 2.25 * i + dsp.rand(-1.0, 1.0) for i in range(1, 2)], dsp.stf(160), 'sine', (0.3, dsp.mstf(1500))))

    layers = [dsp.env(layer, 'sine') for layer in layers]
    out += dsp.mix(layers, False)

    out = dsp.write(out, 'duet', True)
    dsp.timer('stop')

class Orc:
    """ Do things, play things """

    def __init__(self):
        self.blur = dsp.read('horn.wav')

    def scrub(self, pitches, length, wtype, sel=(0.0, 44100), out=''):
        layers = []

        for pitch in pitches:
            numcycles = length / dsp.htf(pitch)

            if sel[0] == 'rand':
                fstart = dsp.rand() * dsp.flen(self.blur.data) - dsp.htf(pitch)
            else:
                fstart = sel[0] * dsp.flen(self.blur.data) - dsp.htf(pitch)

            fend = fstart + sel[1]

            if length % dsp.htf(pitch) > 0:
                numcycles += 1

            wtable = dsp.wavetable(wtype, numcycles, fend, fstart)
            layers.append(''.join([dsp.env(dsp.cut(self.blur.data, int(i), dsp.htf(pitch)), 'sine') for i in wtable]))

        out += dsp.mix(layers, True, 2.0)

        return out 
      
if __name__ == '__main__':
    main()
