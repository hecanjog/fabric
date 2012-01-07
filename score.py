#!/usr/bin/env python2
# -*- coding: UTF-8 -*-

import fabric.fabric as dsp

def main(out=''):
    dsp.timer('start') 
    dsp.snddir = 'sounds/'

    score = Score()

    out += score.opening()

    out = dsp.write(out, 'render', True)

    dsp.timer('stop')

class Score:
    """ structure, score """

    def opening(self, out=''):
        out += dsp.tone(dsp.stf(10), 440, 'sine2pi', 0.3)
        
        return out

        

      
if __name__ == '__main__':
    main()
