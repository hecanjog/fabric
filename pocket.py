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

    opening = score.opening(dsp.stf(120))

    pings = dsp.mix([score.pings(dsp.mstf(100), dsp.stf(40), (50 * 2**6, 75 * 2**6)), score.pings(dsp.mstf(101), dsp.stf(40), (50 * 2**6, 75 * 2**6))])

    out += dsp.mix([opening, score.bells_opening(), dsp.env(pings, 'line')], False)
    print 'generated', dsp.cycle_count, 'cycles'

    #out += dsp.mix([score.bells_opening(), dsp.fill(pings, dsp.stf(26.5))])
    out += dsp.mix([score.bells_opening(), dsp.env(dsp.mix([score.swells_opening(dsp.stf(27), 150 * 3), score.swells_opening(dsp.stf(27), 175 * 3)]), 'line'), dsp.fill(pings, dsp.stf(26.5))], False)
    out += dsp.mix([score.bells_opening(), dsp.env(dsp.mix([score.swells_opening(dsp.stf(27), 150 * 3), score.swells_opening(dsp.stf(27), 175 * 3)]), 'phasor'), dsp.fill(pings, dsp.stf(26.5))], False)

    out = dsp.write(out, 'render', True)

    # Show render time
    timer = time.time() - timer
    min = int(timer) / 60
    sec = timer - (min * 60)
    print 'render time:', min, 'min', sec, 'sec'

class Score:
    """ structure, score """

    def pings(self, grain_size, length, freqs, out=''):
        print 'ping!', grain_size, length, freqs
        tone = dsp.tone(grain_size, freqs[0], 'sine2pi', 0.05)
        tone2 = dsp.tone(grain_size, freqs[1], 'saw', 0.05)
        print type(tone)
        tone = dsp.mix([tone, tone2])
        out += ''.join([dsp.pulsar(tone, (1.0, 1.05, 'random'), (1.0, 1.0, 'line'), random.random()) for i in range(length / dsp.flen(tone))])
        return out

    def opening(self, length, amp=0.5, env_type='sine2pi', out=''):
        print 'opening!', length, env_type
        cluster = dsp.mix([dsp.tone(dsp.stf(4.5), 50, 'sine2pi', 0.3), dsp.tone(dsp.stf(1.5), 200, 'sine2pi', 0.3), dsp.tone(dsp.stf(1.5), 150, 'sine2pi', 0.3)])
        out += dsp.mix([dsp.env(cluster, 'line'), dsp.tone(dsp.stf(2), 50, 'saw', 0.1)], False)
        out += ''.join([dsp.byte_string(random.randint(0, 3000)) for i in range(441)])
        out += dsp.pad('', dsp.stf(1), 0)

        salty = random.random() * 0.01
        env_type = 'saw'
        low = dsp.mix([dsp.env(dsp.tone(length, (i+1)*25.0 + salty, env_type, amp), 'sine') for i in range(8)])
        mid = dsp.mix([dsp.env(dsp.tone(length, (i+1)*75.1 + salty, env_type, amp), 'sine') for i in range(24)])
        env_type = 'random'
        high = dsp.mix([dsp.env(dsp.tone(length, (i+1)*50.05 + salty, env_type, amp), 'sine') for i in range(24)])
        higher = dsp.mix([dsp.env(dsp.tone(length, (i+1)*100.05 + salty, env_type, amp), 'sine') for i in range(12)])

        out += dsp.amp(dsp.mix([low,mid, dsp.env(dsp.mix([high, higher]), 'line')]), 0.7)
        
        return out

    def swells_opening(self, length, pitch, out=''):
        out += dsp.mix([dsp.pulsar(dsp.tone(length, pitch, 'sine2pi', 0.15), (1.0, 1.05, 'random'), (0.6, 1.0, 'vary'), random.random()) for i in range(3)])

        return out

    def bells_opening(self, out=''):

        notes = [
            [(200, dsp.stf(3), 0.3), (199, dsp.stf(5.8), 0.4), (75, dsp.stf(4), 0.3)],
            [(100, dsp.stf(3), 0.3), (201, dsp.stf(5.8), 0.4), (150, dsp.stf(3), 0.2)],
            [(50, dsp.stf(3), 0.3), (300, dsp.stf(5.8), 0.4), (75 / 2, dsp.stf(3), 0.3)],
        ]

        streams = [self.bell_stream(n) for n in notes]
        out += dsp.mix(streams)

        notes[0][1] = (175, dsp.stf(5), 0.35)
        notes[1][1] = (175 / 2, dsp.stf(5), 0.4)
        notes[2][1] = (175 * 2, dsp.stf(5), 0.3)

        notes[0][2] = (130, dsp.stf(3), 0.35)
        notes[1][2] = (130 / 2, dsp.stf(3), 0.35)
        notes[2][2] = (130 * 2, dsp.stf(3), 0.35)
        streams = [self.bell_stream(n) for n in notes]
        out += dsp.mix(streams)

        notes[0][1] = (199, dsp.stf(6.5), 0.35)
        notes[1][1] = (201 / 2, dsp.stf(6.5), 0.4)
        notes[2][1] = (300 * 2, dsp.stf(6.5), 0.3)

        notes[0][2] = (75, dsp.stf(5), 0.3)
        notes[1][2] = (150, dsp.stf(5), 0.3)
        notes[2][2] = (75 / 2, dsp.stf(5), 0.3)
        streams = [self.bell_stream(n) for n in notes]
        out += dsp.mix(streams)

        notes[0][0] = (130 / 2, dsp.stf(5), 0.35)
        notes[1][0] = (130, dsp.stf(4), 0.4)
        notes[2][0] = (130 / 4, dsp.stf(4), 0.3)

        notes[0][2] = (120, dsp.stf(8), 0.4)
        notes[1][2] = (120 / 2, dsp.stf(8), 0.4)
        notes[2][2] = (120 / 4, dsp.stf(8), 0.4)

        notes[0][1] = (199, dsp.stf(4), 0.3)
        notes[1][1] = (201, dsp.stf(4), 0.3)
        notes[2][1] = (300, dsp.stf(4), 0.3)

        streams = [self.bell_stream(n) for n in notes]
        out += dsp.mix(streams)

        return out

    def bell_stream(self, notes):
        bells = [self.bell(n[0], n[1], n[2]) for n in notes]
        return ''.join(bells)

    def bell(self, freq, length, amp):
        bell = dsp.tone(length, freq, 'sine2pi', amp)
        bell = dsp.mix([dsp.pulsar(bell, (1.0, 1.008, 'random'), (0.0, 1.0, 'phasor'), random.random()) for i in range(10)], True, 2.0)

        return bell
        
        

      
if __name__ == '__main__':
    main()
