#!/usr/bin/env python2
# -*- coding: UTF-8 -*-

import fabric.fabric as dsp
import random
import time

def main(out=''):
    timer = time.time()

    dsp.snddir = 'sounds/magill_interlude/'
    magill = Magill()
    dsp.beat = dsp.bpm2frames(88.0)

    out += magill.test()

    print dsp.write(out, 'magill')

    # Show render time
    timer = time.time() - timer
    min = int(timer) / 60
    sec = timer - (min * 60)
    print 'render time:', min, 'min', sec, 'sec'

class Magill:
    """ structure, score """

    def __init__(self):
        self.patterns = Patterns()

        # preload sounds
        self.aa = dsp.read('wes01.wav')

        # Set audio params
        dsp.audio_params = self.aa.params

    def test(self, out=''):
        
        return out

class Patterns:
    """ recipes, patterns """

    def pulsar(self, out=''):
        
        return out
            
if __name__ == '__main__':
    main()
