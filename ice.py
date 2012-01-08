#!/usr/bin/env python2
# -*- coding: UTF-8 -*-

import fabric.fabric as dsp

def main(out=''):
    dsp.timer('start') 
    dsp.snddir = 'sounds/disquiet0001-ice/'
    dsp.seed('disquiet0001-ice')

    score = Score()

    out += dsp.mix([score.glaciers(score.ice.data), dsp.env(score.resonators(score.ice.data, [[98, 196], [98, 200]]), 'line')], False, 2.5)

    pitches = [
        [440, 660, 440 * 4, 440 * 8],
        [220, 440, 660, 440 * 4, 440 * 8],
        [110, 220, 440, 550 * 2],
        [110, 220, 440, 550, 550 * 2],
        [55, 220, 440, 880, 440 * 4],
        [55, 220, 440, 660, 880, 440 * 4],
    ]
   
    out += score.resonators(score.ice.data, pitches) 
    out += score.slivers(score.resonators(score.ice.data, pitches))
    out += score.glaciers(score.ice.data)

    out = dsp.write(out, 'render', True)

    dsp.timer('stop')

class Score:
    """ structure, score """

    def __init__(self):
        self.ice = dsp.read('ice.wav')

    def resonators(self, sound, pitches, out=''):
        pitches = [[dsp.htf(p) for p in pitch] for pitch in pitches]
    
        out += dsp.mix([dsp.pad(self.reson(sound, p), dsp.stf(dsp.rand(0.0, 4.0)), 0) for p in pitches])

        return out


    def reson(self, sound, pitches, out=''):
        streams = [dsp.split(sound, p) for p in pitches]
        streams = [''.join([dsp.env(g, 'sine') for g in s]) for s in streams]

        out += dsp.mix([dsp.env(s, 'vary') for s in streams])

        return out 

    def glaciers(self, sound, out=''):
        
        # Glaciers
        freq = (0.75, 0.85, 'vary')
        amp = (0.0, 1.0, 'vary')
        out += dsp.mix([ dsp.env(dsp.pulsar(sound, freq, amp, dsp.rand()), 'vary') for i in range(10) ], True, 5.0)
        
        return out

    def slivers(self, sound, out=''):

        # Slivers
        slivers = [dsp.cut(sound, dsp.randint(0, dsp.flen(self.ice.data) - dsp.mstf(220)), dsp.mstf(dsp.randint(40, 220))) for i in range(20)]
        slivers = [dsp.pad(dsp.env(s, 'phasor'), dsp.randint(0, 24) * dsp.mstf(10), dsp.randint(0, 24) * dsp.mstf(10)) * 100 for s in slivers]

        out += dsp.mix([dsp.panenv(s, 'vary', 'vary') for s in slivers], True, 5.0)

        return out


        

      
if __name__ == '__main__':
    main()
