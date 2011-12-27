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

    out += score.section(dsp.stf(27))

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

    def section(self, length, out=''):
        layers = []

        layers.append(self.sines(length))
        layers.append(self.sines(length))

        out += dsp.mix(layers) 
        
        return out

    def trains(self, out=''):

        return out

    def sines(self, length, out=''):
        layers = [ dsp.tone( length 
                            ,self.pitches[dsp.randint(0,4)] 
                            ,'sine2pi' 
                            ,dsp.rand(0.01, 0.2) ) 
                   for i in range(dsp.randint(3,6)) ]

        out += dsp.mix(layers)
        
        return out

        

      
if __name__ == '__main__':
    main()
