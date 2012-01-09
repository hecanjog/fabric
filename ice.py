#!/usr/bin/env python2
# -*- coding: UTF-8 -*-

import fabric.fabric as dsp

""" Olive oil gets everywhere!
    www.hecanjog.com (CC) BY-NC-SA 
"""

def main(out=''):
    dsp.timer('start') 
    dsp.snddir = 'sounds/disquiet0001-ice/'
    dsp.seed('disquiet0001-ice')

    orc = Orc()

    pitches = [
        [218.02, 327.03, 490.55], # A E B
        [196.22, 294.33, 490.55], # G D B
        [174.42, 294.33, 436.04], # F D A
        [145.35, 294.33, 294.33 * 2], # D D D 
    ]

    out += ''.join([dsp.mix([''.join([orc.icebells(dsp.mstf(dsp.randint(10, 1000)), p) for i in range(dsp.randint(20, 100))]) for p in pitches]) for i in range(3)])

    out = dsp.write(out, 'olive-oil-gets-nowhere')

    dsp.timer('stop')

class Orc:
    """ How to ding, how to dong """

    def __init__(self):
        self.ice = dsp.read('ice.wav')

    def icebells(self, length, pitches, out=''):
        out += dsp.mix([self.icebell(length, p) for p in pitches]) 

        return out

    def icebell(self, length, pitch, out=''):
        numcycles = length / dsp.htf(pitch)

        if length % dsp.htf(pitch) > 0:
            numcycles += 1

        offset = dsp.randint(0, 44100)

        out += ''.join([dsp.env(dsp.cut(self.ice.data, i + offset, dsp.htf(pitch)), 'sine') for i in range(numcycles)])

        return out 

      
if __name__ == '__main__':
    main()
