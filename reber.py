#!/usr/bin/env python2
# -*- coding: UTF-8 -*-

import fabric.fabric as dsp

def main(out=''):
    dsp.timer('start') 
    dsp.snddir = 'sounds/reber/'

    orc = Orc()

    out += orc.scrub([100 * i for i in range(1, 40)], dsp.stf(200), 'line')
    out += orc.scrub([300 * i for i in range(1, 40)], dsp.stf(200), 'phasor')
    out += orc.scrub([600 * i for i in range(1, 10)], dsp.stf(200), 'line')
    out += orc.scrub([600 * i for i in range(1, 20)], dsp.stf(200), 'phasor')

    out += dsp.mix([orc.expand(dsp.stf(3), 16, dsp.htf(9.5 * i), dsp.htf(300.5 * i)) for i in range(1, 10)], False)

    out = dsp.write(out, 'blur', True)
    dsp.timer('stop')

class Orc:
    """ Do things, play things """

    def __init__(self):
        self.blur = dsp.read('blur3.wav')

    def expand(self, length, grid, longest, shortest, out=''):
        out += ''.join([dsp.env(dsp.cut(self.blur.data, i * grid, v), 'sine', True) for i,v in enumerate(dsp.wavetable('random', length / grid, longest, shortest))])

        return out

    def scrub(self, pitches, length, wtype, out=''):
        layers = []

        for pitch in pitches:
            numcycles = length / dsp.htf(pitch)

            if length % dsp.htf(pitch) > 0:
                numcycles += 1

            wtable = dsp.wavetable(wtype, numcycles, dsp.flen(self.blur.data) - dsp.htf(pitch), 0.0) 
            layers.append(''.join([dsp.env(dsp.cut(self.blur.data, int(i), dsp.htf(pitch)), 'sine') for i in wtable]))

        out += dsp.mix(layers)

        return out 
      
if __name__ == '__main__':
    main()
