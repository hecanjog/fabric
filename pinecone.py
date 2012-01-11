#!/usr/bin/env python2
# -*- coding: UTF-8 -*-

import fabric.fabric as dsp

def main(out=''):
    dsp.timer('start') 
    dsp.snddir = 'sounds/'

    orc = Orc()

    out += orc.pinecone.data
    out += dsp.pad('', 0, dsp.mstf(500)) # silence

    #out += orc.scrub([440, 660, 880], dsp.stf(0.5), 'line')
    #out += orc.scrub([330, 660, 990], dsp.stf(0.5), 'line')
    #out += orc.scrub([440, 500, 700], dsp.stf(0.5), 'line')
    #out += orc.scrub([440, 600, 880], dsp.stf(1), 'line')

    #out += orc.scrub([550, 660, 770], dsp.stf(4), 'tri')
    #out += orc.scrub([550, 660, 770], dsp.stf(3), 'phasor')

    #out += orc.scrub([440, 660, 880], dsp.stf(2), 'sine')
    #out += orc.scrub([330, 660, 990], dsp.stf(3), 'cos')
    #out += orc.scrub([440, 500, 700], dsp.stf(4), 'cos')
    #out += orc.scrub([440, 600, 880], dsp.stf(5), 'sine')

    #out += orc.scrub([420, 600, 890], dsp.stf(6), 'cos')
    #out += orc.scrub([400, 600, 900], dsp.stf(9), 'sine')

    #out += orc.scrub([400, 600, 900], dsp.stf(10), 'vary')

    out += orc.expand()

    out += orc.pinecone.data

    out = dsp.write(out, 'pinecone', True)
    dsp.timer('stop')

class Orc:
    """ Do things, play things """

    def __init__(self):
        self.pinecone = dsp.read('pinecone.wav')

    def expand(self, out=''):
        scrublen = dsp.stf(1)
        grid = 16 

        out += ''.join([dsp.env(dsp.cut(self.pinecone.data, i * grid, v), 'sine', True) for i,v in enumerate(dsp.wavetable('tri', scrublen / grid, dsp.mstf(10), 3))])

        return out

    def scrub(self, pitches, length, wtype, lowpos=0.0, highpos=1.0, out=''):
        layers = []


        for pitch in pitches:
            numcycles = length / dsp.htf(pitch)

            if length % dsp.htf(pitch) > 0:
                numcycles += 1

            # Only reads through the first half of the sample
            wtable = dsp.wavetable(wtype, numcycles, 0.5 * (dsp.flen(self.pinecone.data) - dsp.htf(pitch)), 0.0) 
            layers.append(''.join([dsp.env(dsp.cut(self.pinecone.data, int(i), dsp.htf(pitch)), 'sine') for i in wtable]))

        out += dsp.mix(layers)

        return out 
      
if __name__ == '__main__':
    main()
