#!/usr/bin/env python2
# -*- coding: UTF-8 -*-

import fabric.fabric as dsp

def main(out=''):
    dsp.timer('start') 
    dsp.snddir = 'sounds/disquiet0001-ice/'
    dsp.seed('disquiet0001-ice')

    score = Score()
    
    out += score.glaciers(score.ice.data)
    out += score.resonators(score.ice.data) 
    out += score.slivers(score.resonators(score.ice.data))
    out += score.glaciers(score.ice.data)

    out = dsp.write(out, 'render', True)

    dsp.timer('stop')

class Score:
    """ structure, score """

    def __init__(self):
        self.ice = dsp.read('ice.wav')

    def resonators(self, sound, out=''):
        pitches = [
            [220, 440, 660],
            [110, 220, 440, 550],
            [55, 220, 440, 660],
        ]

        pitches = [[dsp.htf(p) for p in pitch] for pitch in pitches]
        sectionlen = dsp.flen(sound) / len(pitches)

        sounds = dsp.split(sound, sectionlen)
    
        out += ''.join([self.reson(s, pitches[i]) for i,s in enumerate(sounds)])

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
        out += dsp.mix([ dsp.env(dsp.pulsar(sound, freq, amp, dsp.rand()), 'vary') for i in range(10) ], 5.0)
        
        return out

    def slivers(self, sound, out=''):

        # Slivers
        slivers = [dsp.cut(sound, dsp.randint(0, dsp.flen(self.ice.data) - dsp.mstf(20)), dsp.mstf(dsp.randint(10, 60))) for i in range(7)]
        slivers = [dsp.pad(dsp.env(s, 'random'), dsp.randint(0, 16) * dsp.mstf(10), dsp.randint(0, 16) * dsp.mstf(10)) * 280 for s in slivers]

        out += dsp.mix([dsp.panenv(s, 'vary', 'vary') for s in slivers], 5.0)

        return out


        

      
if __name__ == '__main__':
    main()
