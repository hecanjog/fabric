#!/usr/bin/env python2
# -*- coding: UTF-8 -*-

import fabric.fabric as dsp

""" Olive oil gets nowhere!
    www.hecanjog.com (CC) BY-NC-SA 
"""

def main(out=''):
    dsp.timer('start') 
    dsp.snddir = 'sounds/disquiet0001-ice/'
    dsp.seed('disquiet0001-ice')

    orc = Orc()

    pitchgroups = [
        [dsp.stf(100), 218.02, 327.03, 490.55], # A E B
        [dsp.stf(80), 196.22, 294.33, 490.55], # G D B
        [dsp.stf(90), 174.42, 294.33, 436.04], # F D A
        [dsp.stf(120), 145.35, 294.33, 294.33 * 2], # D D D 
    ]

    layers = []

    for pitches in pitchgroups:
        length = pitches[0]
        tlengths = []
        while sum(tlengths) < length:
            tlengths.append(dsp.randint(dsp.mstf(10000), dsp.mstf(100)))

        pitches.pop(0)
        layer =''
        for p in pitches:
            layer += dsp.mix([''.join([orc.icebell(length, p) for length in dsp.randshuffle(tlengths)]) for i in range(6)])

        layers.append(layer)

    icelayers = [dsp.env(l, 'vary') for l in layers]
    icelayers = [dsp.amp(dsp.env(l, 'sine'), 0.3) for l in icelayers]
    layers = [dsp.env(l, 'sine') for l in layers]
    layers.extend(icelayers)
    out += dsp.mix(layers, 6.0)

    out = dsp.write(out, 'olive-oil-gets-nowhere')

    dsp.timer('stop')

class Orc:
    """ How to ding, how to dong """

    def __init__(self):
        self.ice = dsp.read('ice.wav')

    def icebell(self, length, pitch, out=''):
        numcycles = length / dsp.htf(pitch)

        if length % dsp.htf(pitch) > 0:
            numcycles += 1

        offset = dsp.randint(0, 44100)

        out += ''.join([dsp.env(dsp.cut(self.ice.data, i + offset, dsp.htf(pitch)), 'sine') for i in range(numcycles)])

        return out 

      
if __name__ == '__main__':
    main()
