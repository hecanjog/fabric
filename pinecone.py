#!/usr/bin/env python2
# -*- coding: UTF-8 -*-

import fabric.fabric as dsp

def main(out=''):
    dsp.timer('start') 
    dsp.snddir = 'sounds/'
    dsp.seed('pinecone')

    orc = Orc()

    out += orc.pinecone.data
    out += dsp.pad('', 0, dsp.mstf(500)) # silence

    out += orc.scrub([440, 660, 880], 100)
    out += dsp.pad('', 0, dsp.mstf(500)) # silence

    out += orc.scrub([440, 660, 880], 50)
    out += dsp.pad('', 0, dsp.mstf(500)) # silence

    out += orc.scrub([440, 660, 880], 40)
    out += dsp.pad('', 0, dsp.mstf(500)) # silence
    
    out += orc.scrub([440, 660, 880], 30)
    out += dsp.pad('', 0, dsp.mstf(500)) # silence

    out += orc.scrub([440, 660, 880], 20)
    out += dsp.pad('', 0, dsp.mstf(500)) # silence

    out += orc.scrub([440, 660, 880], 15)
    out += dsp.pad('', 0, dsp.mstf(500)) # silence

    out += orc.scrub([440, 660, 880], 10)
    out += dsp.pad('', 0, dsp.mstf(500)) # silence

    out += orc.scrub([440, 660, 880], 8)
    out += dsp.pad('', 0, dsp.mstf(500)) # silence

    out += orc.scrub([440, 660, 880], 4)
    out += dsp.pad('', 0, dsp.mstf(500)) # silence

    out += orc.scrub([440, 660, 880], 2)
    out += dsp.pad('', 0, dsp.mstf(500)) # silence

    out += orc.scrub([440, 660, 880], 1)

    out = dsp.write(out, 'pinecone', False)

    dsp.timer('stop')

class Orc:
    """ Do things, play things """

    def __init__(self):
        self.pinecone = dsp.read('pinecone.wav')

    def scrub(self, pitches, interval, out=''):
        layers = []

        for pitch in pitches:
            numcycles = (dsp.flen(self.pinecone.data) - dsp.htf(pitch)) / interval 
            layers.append(''.join([dsp.env(dsp.cut(self.pinecone.data, i * interval, dsp.htf(pitch)), 'sine') for i in range(numcycles)]))

        out += dsp.mix(layers)

        return out 

      
if __name__ == '__main__':
    main()
