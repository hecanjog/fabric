#!/usr/bin/env python2
# -*- coding: UTF-8 -*-

import fabric.fabric as dsp

def main(out=''):
    """ sending dreams to she downstream """
    dsp.timer('start')
    dsp.seed('pocket')

    dsp.snddir = 'sounds/'
    orc = Orc()

    layers = []
    layers.append(orc.pings(dsp.mstf(100), dsp.stf(40), (50 * 2**6, 75 * 2**6)))
    layers.append(orc.pings(dsp.mstf(101), dsp.stf(40), (50 * 2**6, 75 * 2**6)))
    layers = [dsp.env(dsp.mix(layers), 'line')] # Mix and envelope pings down to layer 0 
    layers.append(orc.opening(dsp.stf(120)))
    layers.append(orc.bells_opening())
    out += dsp.mix(layers, False)

    layers = []
    layers.append(orc.phasesaw(dsp.stf(60), 32.7, 0.15, 1.03))
    layers.append(orc.bells_opening())
    layers.append(orc.pings(dsp.mstf(100), dsp.stf(60), (50 * 2**6, 80 * 2**6)))
    layers.append(orc.pings(dsp.mstf(101), dsp.stf(60), (50 * 2**6, 80 * 2**6)))
    out += dsp.mix(layers)

    layers = []
    layers.append(orc.phasesaw(dsp.stf(60), 65.4 * 0.5, 0.1, 1.01))
    layers.append(orc.bells_opening())
    layers.append(orc.pings(dsp.mstf(100), dsp.stf(60), (50 * 2**6, 80 * 2**6)))
    layers.append(orc.pings(dsp.mstf(101), dsp.stf(60), (50 * 2**6, 80 * 2**6)))
    out += dsp.mix(layers)

    out = dsp.write(out, 'pocket', True)
    dsp.timer('stop')


class Orc:
    """ make sound """

    def phasesaw(self, length, tonic, drift_width, drift_speed, harmony=150.0, out=''):
        layers = []
        layers.append(self.swells(length, harmony * 1.5))
        layers.append(self.swells(length, (harmony / 6 + harmony) * 1.5))
        layers = [dsp.env(dsp.mix(layers), 'line')] # Mix and enveloping swells down to layer 0

        layers.extend([self.swells(length, tonic * i, 'saw', drift_width, drift_speed) for i in range(4)])

        out += dsp.mix(layers)

        return out

    def pings(self, grain_size, length, freqs, out=''):
        print 'ping!', grain_size, length, freqs
        tone = dsp.tone(grain_size, freqs[0], 'sine2pi', 0.05)
        tone2 = dsp.tone(grain_size, freqs[1], 'saw', 0.05)
        tone = dsp.mix([tone, tone2])
        out += ''.join([dsp.pulsar(tone, (1.0, 1.05, 'random'), (1.0, 1.0, 'line'), dsp.rand()) for i in range(length / dsp.flen(tone))])
        return out

    def opening(self, length, amp=0.5, env_type='sine2pi', out=''):
        print 'opening!', length, env_type

        low = dsp.mix([dsp.env(dsp.tone(length, (i+1)*25.0 + dsp.rand(0.0, 0.01), 'saw', amp), 'sine') for i in range(8)])
        mid = dsp.mix([dsp.env(dsp.tone(length, (i+1)*75.1 + dsp.rand(0.0, 0.01), 'saw', amp), 'sine') for i in range(24)])

        high = dsp.mix([dsp.env(dsp.tone(length, (i+1)*50.05 + dsp.rand(0.0, 0.01), 'random', amp), 'sine') for i in range(24)])
        higher = dsp.mix([dsp.env(dsp.tone(length, (i+1)*100.05 + dsp.rand(0.0, 0.01), 'random', amp), 'sine') for i in range(12)])

        out += dsp.amp(dsp.mix([low,mid, dsp.env(dsp.mix([high, higher]), 'line')]), 0.7)
        
        return out

    def swells(self, length, pitch, env='sine2pi', amp=0.15, fmod=1.05, out=''):
        out += dsp.mix([dsp.pulsar(dsp.tone(length, pitch, env, amp), (1.0, fmod, 'random'), (0.6, 1.0, 'vary'), dsp.rand()) for i in range(3)])
        out = dsp.fill(out, length)
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

        streams = [self.bell_stream(n, 2.0) for n in notes]
        out += dsp.mix(streams)

        return out

    def bell_stream(self, notes, mult=1.0):
        bells = [self.bell(n[0] * mult, n[1], n[2]) for n in notes]
        return ''.join(bells)

    def bell(self, freq, length, amp):
        bell = dsp.tone(length, freq, 'sine2pi', amp)
        bell = dsp.mix([dsp.pulsar(bell, (1.0, 1.008, 'random'), (0.0, 1.0, 'phasor'), dsp.rand()) for i in range(10)], True, 2.0)

        return bell

      
if __name__ == '__main__':
    main()
