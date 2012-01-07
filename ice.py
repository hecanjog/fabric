#!/usr/bin/env python2
# -*- coding: UTF-8 -*-

import fabric.fabric as dsp

def main(out=''):
    dsp.timer('start') 
    dsp.snddir = 'sounds/disquiet0001-ice/'
    dsp.seed('disquiet0001-ice')

    score = Score()

    out += score.opening()

    out = dsp.write(out, 'render', True)

    dsp.timer('stop')

class Score:
    """ structure, score """

    def __init__(self):
        self.ice = dsp.read('ice.wav')

    def opening(self, out=''):
        freq = (0.2, 2.0, 'vary')
        amp = (0.0, 1.0, 'vary')
        out += dsp.mix([ dsp.env(dsp.pulsar(self.ice.data, freq, amp, dsp.rand()), 'vary') for i in range(10) ], 5.0)
        
        return out

        

      
if __name__ == '__main__':
    main()
