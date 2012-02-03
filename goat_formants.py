#!/usr/bin/env python2
# -*- coding: UTF-8 -*-

import fabric.fabric as dsp

def main(out=''):
    """ www.hecanjog.com :: (cc) by-nc-sa """
    
    # Put william.wav into the sounds directory before running!
    # Download it here: sounds.hecanjog.com/william.wav

    dsp.timer('start') 
    dsp.snddir = 'sounds/'
    dsp.seed('goat formants')

    orc = Orc()

    tonic = 110.0
    llen = dsp.stf(1010)
    layers = []

    # Opening high tones
    hi = orc.scrub([tonic * 2, tonic * 3, tonic * 6], int(llen * 0.25), 'random', (0.0, 0.5))
    hi = dsp.split(hi, int(llen * 0.0125))
    hi = ''.join(dsp.randshuffle(hi))
    hi = dsp.mix([orc.scrub([tonic * 3, tonic * 2], int(llen * 0.25), 'sine', (0.0, 0.4), 'random'), hi])
    hi = dsp.env(hi, 'sine')
    hi = dsp.pad(hi, 0, int(llen * 0.74))
    layers.append(hi)

    # Opening tones P1, P8, P12
    subgroup = []
    subgroup.append(orc.scrub([tonic + dsp.rand(-1.0, 1.0)], int(llen * 1.0), 'sine', (0.0, 0.3)))
    subgroup.append(orc.scrub([tonic * 2 + dsp.rand(-1.0, 1.0) ], int(llen * 0.95), 'sine', (0.4, 0.4)))
    subgroup.append(orc.scrub([tonic * 3 + dsp.rand(-1.0, 1.0) ], int(llen * 0.97), 'sine', (0.02, 0.2)))
    layers.append(dsp.env(dsp.mix(subgroup, False, 4.0), 'sine'))
   
    # Middle tones, rougher P5, P8
    subgroup = []
    subgroup.append(orc.scrub([tonic * 1.5 * i + dsp.rand(-1.0, 1.0) for i in range(1, 3)], int(llen * 0.7), 'sine', (0.3, 0.75)))
    subgroup.append(orc.scrub([tonic * 2 * i + dsp.rand(-1.0, 1.0) for i in range(1, 2)], int(llen * 0.7), 'sine', (0.35, 0.4), 'gauss'))
    subgroup.append(orc.scrub([tonic * 2 * i + dsp.rand(-1.0, 1.0) for i in range(1, 2)], int(llen * 0.75), 'sine', (0.4, 0.5), 'phasor'))
    layers.append(dsp.env(dsp.mix(subgroup, False, 4.0), 'sine'))

    # End tones, M3, M9
    subgroup = []
    subgroup.append(orc.scrub([tonic * 1.25 * i + dsp.rand(-1.0, 1.0) for i in range(1, 3)], int(llen * 0.45), 'phasor', (0.2, 0.1), 'gauss'))
    subgroup.append(orc.scrub([tonic * 2.25 * i + dsp.rand(-1.0, 1.0) for i in range(1, 2)], int(llen * 0.55), 'sine', (0.4, 0.3), 'random'))
    subgroup.append(orc.scrub([tonic * 2.25 * i + dsp.rand(-1.0, 1.0) for i in range(1, 2)], int(llen * 0.5), 'sine', (0.5, 0.4), 'random'))
    subgroup = [dsp.split(s, dsp.mstf(80 + (i*2))) for s in subgroup]
    subgroup = [''.join(dsp.randshuffle(s)) for s in subgroup]
    layers.append(dsp.env(dsp.mix(subgroup, False, 4.0), 'sine'))

    # Coda tones, low tonics
    subgroup = []
    subgroup.append(orc.scrub([tonic * 0.25, tonic * 0.125], int(llen * 0.2), 'line', (0.35, 0.1)))
    subgroup.append(orc.scrub([tonic * 0.25, tonic * 0.5], int(llen * 0.2), 'line', (0.37, 1.0), 'random'))
    layers.append(dsp.env(dsp.mix(subgroup, False, 4.0), 'sine'))

    thesun = orc.scrub([tonic * 50, tonic, tonic * 49, tonic * 48, tonic * 24 ], dsp.stf(10), 'sine', (0.32, 0.4), 'random')
    suns = dsp.mix([orc.burstsun(dsp.amp(thesun, 0.9), int(llen * 1.0)) for i in range(6)])

    out += dsp.mix([dsp.mix(layers, False, 4.0), suns], False)

    out = dsp.write(out, 'goat_formants', False)
    dsp.timer('stop')

class Orc:
    """ Do things, play things """

    def __init__(self):
        self.horn = dsp.read('william.wav')

    def burstsun(self, snd, length, out=''):
        numtimes = int(length / dsp.mstf(1000))
        ptable = dsp.wavetable('sine', numtimes, dsp.flen(snd) - dsp.mstf(100), 0)
        ltable = dsp.breakpoint([['random', dsp.randint(dsp.mstf(80), dsp.mstf(1000))] for i in range(numtimes / 40)], numtimes)
        horns = [dsp.pad(dsp.env(dsp.cut(snd, int(ptable[i]), int(ltable[i])), 'sine', True), 0, dsp.randint(int(i * 0.05), int(i * 0.5))) for i in range(numtimes)]

        out += dsp.fill(dsp.pulsar(''.join(horns)), length)

        return out

    def scrub(self, pitches, length, wtype, sel=(0.0, 1.0), gtype='sine', out=''):
        layers = []

        for pitch in pitches:
            numcycles = length / dsp.htf(pitch)

            if sel[0] == 'rand':
                fstart = dsp.rand() * dsp.flen(self.horn.data) - dsp.htf(pitch)
            else:
                fstart = sel[0] * dsp.flen(self.horn.data) - dsp.htf(pitch)

            fend = int(fstart + sel[1] * (dsp.flen(self.horn.data) - dsp.htf(pitch) - fstart))

            if length % dsp.htf(pitch) > 0:
                numcycles += 1

            wtable = dsp.wavetable(wtype, numcycles, fend, fstart)
            layers.append(''.join([dsp.env(dsp.cut(self.horn.data, int(i), dsp.htf(pitch)), gtype) for i in wtable]))

        out += dsp.mix(layers, True, 2.0)

        return out 
      
if __name__ == '__main__':
    main()
