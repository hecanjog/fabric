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
    dsp.beat = dsp.bpm2frames(88.0)

    rough = dsp.mix([score.opening(dsp.stf(360), 'random') for i in range(3)])
    roughy = dsp.mix([score.opening(dsp.stf(360), 'line') for i in range(3)])
    smooth = dsp.mix([score.opening(dsp.stf(360), 'sine') for i in range(3)])
    out += dsp.mix([rough, roughy, smooth], False, 0.8)

    out = dsp.write(out, 'render', True)

    # Show render time
    timer = time.time() - timer
    min = int(timer) / 60
    sec = timer - (min * 60)
    print 'render time:', min, 'min', sec, 'sec'

class Score:
    """ structure, score """

    def __init__(self):
        # Set audio params
        dsp.audio_params = dsp.default_params 

    def opening(self, length, type='sine', out=''):
        salty = random.random() * 0.01
        low = dsp.mix([dsp.env(dsp.tone(length, (i+1)*50.0 + salty, type, random.random() * 0.2), 'sine') for i in range(6)])
        mid = dsp.mix([dsp.env(dsp.tone(length, (i+1)*75.1 + salty, type, random.random() * 0.2), 'sine') for i in range(6)])
        out += dsp.mix([low,mid])
        
        return out

      
if __name__ == '__main__':
    main()
