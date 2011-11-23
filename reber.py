#!/usr/bin/env python2
# -*- coding: UTF-8 -*-

import fabric.fabric as dsp
import random
import time
import audioop 
import math

def main(out=''):
    timer = time.time()

    score = Score()
    dsp.snddir = 'sounds/reber/'
    score.t2 = dsp.read('t2.wav')

    out += score.blur()
    out = dsp.write(out, 'blur', True)

    out = ''
    out += dsp.mix([score.spark(140, 1, 12, 20, 300, 300, 'line') for i in range(12)], False, 3.0)
    out = dsp.write(out, 'sparks-a-line', True)

    out = ''
    out += dsp.mix([score.spark(140, 1, 12, 20, 300, 300, 'vary') for i in range(12)], False, 3.0)
    out = dsp.write(out, 'sparks-a2-breakpoint', True)

    out = ''
    out += dsp.mix([score.spark(140, 10, 12, 20, 80, 300, 'line') for i in range(12)], False, 3.0)
    out = dsp.write(out, 'sparks-b-line', True)

    out = ''
    out += dsp.mix([score.spark(40, 10, 20, 2, 40, 300, 'line') for i in range(20)], False, 3.0)
    out = dsp.write(out, 'sparks-c-line', True)

    out = ''
    out += dsp.mix([score.spark(40, 10, 20, 2, 40, 200, 'sine') for i in range(20)], False, 3.0)
    out = dsp.write(out, 'sparks-d-sine', True)

    out = ''
    out += dsp.mix([score.spark(40, 10, 20, 2, 40, 200, 'vary') for i in range(20)], False, 3.0)
    out = dsp.write(out, 'sparks-d2-breakpoint', True)

    out = ''
    out += dsp.mix([score.spark(10, 0.5, 1, 80, 4000, 500, 'vary') for i in range(20)], False, 3.0)
    out = dsp.write(out, 'sparks-d2-breakpoint', True)

    # Show render time
    timer = time.time() - timer
    min = int(timer) / 60
    sec = timer - (min * 60)
    print 'render time:', min, 'min', sec, 'sec'

class Score:
    """ structure, score """

    def spark(self, numsparks=140, lowspeed=1, highspeed=12, minlen=20, maxlen=200, gaplen=400, shape='line', out=''):
        print 'spark!'

        # cut a sequence of variable length short grains

        numsparks = 140
        sparks = []
        section = self.t2.data
        section_length = dsp.stf(6)
        section_start = random.randint(0, dsp.flen(section) - section_length)
        section = dsp.cut(section, section_start, section_length)
        for i in range(numsparks):
            spark_length = random.randint(dsp.mstf(minlen), dsp.mstf(random.randint(minlen, maxlen)))
            spark_start = random.randint(0, dsp.flen(section) - spark_length)
            sparks.append(dsp.cut(section, spark_start, spark_length))

        shape = dsp.wavetable(shape, numsparks)
        sparks = [dsp.pulsar(s, (random.random() * lowspeed + 0.2, random.random() * highspeed + 1.3, 'vary'), (random.random(), 1.0, 'random'), random.random()) for s in sparks] 
        sparks = [dsp.pad(s, 0, dsp.mstf(shape[i] * gaplen)) for i,s in enumerate(sparks)]

        return ''.join(sparks)


    def blur(self, out=''):
        print 'blur!'

        section = dsp.split(self.t2.data, dsp.stf(20))
        section = dsp.mix(section)

        tee = []
        for i in range(6):
            tee = dsp.interleave(tee, dsp.split(section, dsp.mstf(random.randint(40, 100))))

        tee = dsp.packet_shuffle(tee, 4)
        tee = ''.join(tee)

        out += dsp.mix([dsp.pulsar(tee, (1.0, 1.1, 'random'), (1.0, 1.0, 'line'), random.random()) for i in range(4)], True, 4.0)
        return out
       
        

      
if __name__ == '__main__':
    main()
