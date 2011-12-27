#!/usr/bin/env python2
# -*- coding: UTF-8 -*-

import fabric.fabric as dsp
import random
import time
import audioop 
import math

def main(out=''):
    timer = time.time()

    dsp.snddir = 'sounds/'
    score = Score()

    section_lengths = score.section_lengths(dsp.stf(4))

    for l in section_lengths:
        out += score.section(l)

    out = dsp.write(out, 'render', True)

    # Show render time
    timer = time.time() - timer
    min = int(timer) / 60
    sec = timer - (min * 60)
    print 'render time:', min, 'min', sec, 'sec'

class Score:
    """ structure, score """

    pitches = [
        220.0,
        440.0,
        math.sqrt(5) * 220.0,
        math.sqrt(5) * 440.0,
        880.0,
      ]

    ratios = [
        1.0,
        math.sqrt(2),
        2.0,
        math.sqrt(5),
        math.sqrt(8),
      ]

    def section_lengths(self, total_length):
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
                            ,self.pitches[dsp.randint(0,4)] 
                            ,'sine2pi' 
                            ,dsp.rand(0.01, 0.2) )) 
                   for i in range(dsp.randint(3,6)) ]

        out += dsp.mix(layers)
        
        return out

        

      
if __name__ == '__main__':
    main()
