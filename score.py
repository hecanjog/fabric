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

    out += score.opening() 

    out = dsp.write(out, 'render', True)

    # Show render time
    timer = time.time() - timer
    min = int(timer) / 60
    sec = timer - (min * 60)
    print 'render time:', min, 'min', sec, 'sec'

class Score:
    """ structure, score """

    def __init__(self):
        # preload sounds
        self.test = dsp.read('stereotest.wav')

        # Set audio params
        dsp.audio_params = self.test.params

    def opening(self, out=''):
        out += self.test.data
        
        return out

      
if __name__ == '__main__':
    main()
