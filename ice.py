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

    pitches = [145.35 * 0.5, 145.35, 144.3] # D D D
    out += dsp.mix([orc.glaciers(orc.ice.data, (0.75, 0.85, 'vary'), 5.0), dsp.env(orc.icebells(dsp.stf(14), pitches), 'line')], False, 2.5)

    pitches = [
        [218.02 * 0.5, 327.03 * 0.5, 490.55 * 0.5], # A E B
        [196.22 * 0.5, 294.33 * 0.5, 490.55 * 0.5], # G D B
        [174.42 * 0.5, 294.33 * 0.5, 436.04 * 0.5], # F D A
        [145.35 * 0.5, 294.33 * 0.5, 436.04 * 0.5], # D D A
    ]
   
    bells = dsp.amp(''.join([orc.icebells(dsp.stf(12), p) for p in pitches]), 2.0)
    bells = ''.join([dsp.mix([orc.slivers(bells), bells], False), dsp.mix([orc.slivers(bells), bells])])

    out += dsp.mix([bells, dsp.fill(dsp.amp(orc.ice.data, 0.3), dsp.flen(bells))])

    bells = orc.slivers(bells)
    bpitches = [218.02 * 0.5, 218.02, 327.03, 327.03 * 2, 218.02 * 2, 490.55] # A A E E A B
    out += dsp.mix([bells, dsp.fill(dsp.amp(orc.ice.data, 0.25), dsp.flen(bells)), orc.icebells(dsp.flen(bells), bpitches)])

    freq = (0.9, 1.0, 'vary')
    out += orc.glaciers(orc.ice.data, freq, 1.0)
    coda = dsp.mix([dsp.pulsar(''.join([orc.icebells(dsp.stf(20), p) for p in pitches])) for i in range(3)], True, 3.0)

    pitches = [
        [218.02, 327.03, 490.55], # A E B
        [196.22, 294.33, 490.55], # G D B
        [174.42, 294.33, 436.04], # F D A
        [145.35, 294.33, 294.33 * 2], # D D D 
    ]

    out += dsp.mix([''.join([orc.icebells(dsp.stf(20), p) for p in pitches]), coda])
    out += dsp.env(dsp.mix([''.join([orc.icebells(dsp.stf(20), p) for p in pitches]), coda]), 'phasor')

    out = dsp.write(out, 'olive-oil-gets-everywhere')

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

        bell = ''.join([dsp.env(dsp.cut(self.ice.data, i + offset, dsp.htf(pitch)), 'sine') for i in range(numcycles)])

        out += dsp.panenv(bell, 'vary', 'vary')

        return out 

    def glaciers(self, sound, freq, mamp, out=''):
        amp = (0.0, 1.0, 'vary')
        out += dsp.mix([ dsp.env(dsp.pulsar(sound, freq, amp, dsp.rand()), 'vary') for i in range(10) ], True, mamp)
        
        return out

    def slivers(self, sound, out=''):
        slivers = [dsp.cut(sound, dsp.randint(0, dsp.flen(self.ice.data) - dsp.mstf(220)), dsp.mstf(dsp.randint(40, 220))) for i in range(20)]
        slivers = [dsp.pad(dsp.env(s, 'phasor'), dsp.randint(0, 24) * dsp.mstf(10), dsp.randint(0, 24) * dsp.mstf(10)) * 100 for s in slivers]

        out += dsp.mix([dsp.panenv(s, 'vary', 'vary') for s in slivers], True, 10.0)

        return out


        

      
if __name__ == '__main__':
    main()
