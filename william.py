#!/usr/bin/env python2
# -*- coding: UTF-8 -*-

import fabric.fabric as dsp
import random
import audioop 
import math

def main(out=''):
    dsp.timer('start')
    dsp.snddir = 'sounds/'
    score = Score()

    timings = score.timings(dsp.stf(10))

    for t in timings:
        out += score.section(t)

    out = dsp.write(out, 'render', True)

    # Show render time
    dsp.timer('stop')

class Score:
    """ structure, score """

    tonic = 440.0

    pitches = [
        (1.0 / 4.0) * tonic,
        (2.0 / 4.0) * tonic,
        (math.sqrt(5) / 4.0) * tonic,
        (math.sqrt(8) / 4.0) * tonic,
        (3.0 / 4.0) * tonic,
        (4.0 / 4.0) * tonic,
      ]

    ratios = [
        1.0,
        math.sqrt(2),
        2.0,
        math.sqrt(5),
        math.sqrt(8),
      ]

    def timings(self, total_length):
        section_lengths = []
        for r in self.ratios:
            section_lengths.append(int(total_length * r))

        return section_lengths

    def section(self, length, out=''):
        layers = []

        layers.append(self.sines(length))
        layers.append(self.sines(length))

        out += dsp.mix(layers) 
        
        return out

    def trains(self, out=''):

        return out

    def sines(self, length, out=''):
        layers = [ dsp.pulsar(dsp.tone( length 
                            ,self.pitches[dsp.randint(0,len(self.pitches)-1)] 
                            ,'sine2pi' 
                            ,dsp.rand(0.01, 0.2) )) 
                   for i in range(dsp.randint(3,6)) ]

        out += dsp.mix(layers)
        
        return out

        

      
if __name__ == '__main__':
    main()
