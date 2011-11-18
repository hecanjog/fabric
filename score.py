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

    out += score.opening(dsp.stf(500))
    print dsp.cycle_count

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
        print 'opening!', length, type
        salty = random.random() * 0.01
        type = 'line'
        low = dsp.mix([dsp.env(dsp.tone(length, (i+1)*25.0 + salty, type, random.random() * 0.2), 'sine') for i in range(8)])
        mid = dsp.mix([dsp.env(dsp.tone(length, (i+1)*75.1 + salty, type, random.random() * 0.2), 'sine') for i in range(24)])
        type = 'random'
        high = dsp.mix([dsp.env(dsp.tone(length, (i+1)*50.05 + salty, type, random.random() * 0.2), 'sine') for i in range(24)])
        higher = dsp.mix([dsp.env(dsp.tone(length, (i+1)*100.05 + salty, type, random.random() * 0.2), 'sine') for i in range(12)])

        out += dsp.mix([low,mid, dsp.env(dsp.mix([high, higher]), 'line')])
        
        return out

      
if __name__ == '__main__':
    main()
