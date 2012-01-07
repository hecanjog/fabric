#!/usr/bin/env python2
# -*- coding: UTF-8 -*-

import fabric.fabric as dsp

def main(out=''):
    dsp.timer('start') 
    dsp.snddir = 'sounds/disquiet0001-ice/'
    dsp.seed('disquiet0001-ice')

    score = Score()

    out += score.slivers()
    out += score.glaciers()
    out += score.slivers()
    out += score.slivers()
    out += score.glaciers()
    out += score.slivers()

    out = dsp.write(out, 'render', True)

    dsp.timer('stop')

class Score:
    """ structure, score """

    def __init__(self):
        self.ice = dsp.read('ice.wav')

    def glaciers(self, out=''):
        
        # Glaciers
        freq = (0.75, 0.85, 'vary')
        amp = (0.0, 1.0, 'vary')
        out += dsp.mix([ dsp.env(dsp.pulsar(self.ice.data, freq, amp, dsp.rand()), 'vary') for i in range(10) ], 5.0)
        
        return out

    def slivers(self, out=''):

        # Slivers
        slivers = [dsp.cut(self.ice.data, dsp.randint(0, dsp.flen(self.ice.data) - dsp.mstf(20)), dsp.mstf(dsp.randint(10, 60))) for i in range(7)]
        slivers = [dsp.pad(dsp.env(s, 'random'), dsp.randint(0, 16) * dsp.mstf(10), dsp.randint(0, 16) * dsp.mstf(10)) * 280 for s in slivers]

        out += dsp.mix([dsp.panenv(s, 'vary', 'vary') for s in slivers], 5.0)

        return out


        

      
if __name__ == '__main__':
    main()
