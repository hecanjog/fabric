#!/usr/bin/env python2
# -*- coding: UTF-8 -*-

import fabric.fabric as dsp

def main(out='', layers=[]):
    dsp.timer('start')
    dsp.seed('sending dreams to she downstream')

    dsp.snddir = 'sounds/'
    orc = Orc()

    orc.tonic = 75.0

    slen = dsp.stf(80)
    layers = [ orc.slicer(orc.bells_rhythm(slen, [0.5, 1.0]), slen, [2], [1]) ]
    layers += [ orc.slicer(orc.bells_rhythm(slen, [1.5, 2.25]), slen, [2], [1]) ]
    layers += [ orc.slicer(orc.bells_rhythm(slen, [2.25, 3.0]), slen, [2], [1]) ]
    out += dsp.mix(layers, True, 0.12)

    out += dsp.env(dsp.amp(dsp.noise(dsp.stf(1)), 0.2), 'line')
    out += orc.clicks(dsp.stf(0.5), [3], [1])
    out += orc.clicks(dsp.stf(0.25), [2], [1])

    orc.tonic = 74.8

    slen = dsp.stf(40)
    layers = [ orc.slicer(orc.bells_rhythm(slen, [0.5, 1.0]), slen, [4, 2], [1]) ]
    layers += [ orc.slicer(orc.bells_rhythm(slen, [1.5, 2.25]), slen, [4, 2], [1]) ]
    layers += [ orc.slicer(orc.bells_rhythm(slen, [2.25, 3.0]), slen, [4, 2], [1]) ]
    layers = [dsp.amp(l, 0.9) for l in layers]
    layers += [ orc.pings(dsp.mstf(100), dsp.stf(40), (50 * 2**6, 75 * 2**6)) ]
    layers += [ orc.pings(dsp.mstf(101), dsp.stf(40), (50 * 2**6, 75 * 2**6)) ]
    out += dsp.mix(layers, True, 0.7)

    out += orc.clicks(dsp.stf(0.25), [1], [1])
    out += dsp.pad('', 0, dsp.mstf(100))

    ##################
    # A

    slen = dsp.stf(20)
    orc.tonic = 75.0

    layers = [ orc.slicer(orc.bells_rhythm(slen, [0.5, 1.0]), slen, [4, 2], [1,0]) ]
    layers += [ orc.slicer(orc.bells_rhythm(slen, [1.5, 2.5]), slen, [4, 2], [1,0]) ]
    layers += [ orc.slicer(orc.bells_rhythm(slen, [2.5, 3.0]), slen, [4, 2], [1,0]) ]
    layers = [dsp.amp(l, 0.6) for l in layers]

    layers += [ orc.melody(slen, [[4.0, 6.0], [3.0, 5.0]], [6, 4], [1]) ]
    layers += [ orc.melody(slen, [[4.0, 6.666], [2.0, 4.5]], [3, 2], [1]) ]

    layers += [ orc.snares(slen, [3*2*8 for i in range(3)], [0,1]) ]
    layers += [ orc.hat(slen, [3*2*8]) ]
    layers += [ orc.pat(slen, [3*2, 3*2*2, 3*2*3], [0,0,1,0,0,1,1,0,1]) ]
    layers += [ orc.slicer(orc.bells_rhythm(slen, [2.0, 3.0, 1.0]), slen, [3*4*16], [1,0,0]) ]

    out += dsp.mix(layers)

    ##################
    # B

    slen = dsp.stf(31)

    layers = [ orc.slicer(orc.bells_rhythm(slen, [0.5, 1.0]), slen, [4, 8], [1,0]) ]
    layers += [ orc.slicer(orc.bells_rhythm(slen, [1.5, 2.25]), slen, [4, 8], [1,0]) ]
    layers += [ orc.slicer(orc.bells_rhythm(slen, [2.25, 3.0]), slen, [4, 8], [1,0]) ]
    layers = [dsp.amp(l, 0.5) for l in layers]

    layers += [ orc.melody(slen, [[4.0, 6.0], [3.0, 5.0]], [3, 2], [1]) ]
    layers += [ orc.melody(slen, [[4.0, 6.0], [3.0, 5.0]], [6, 12], [0,0,1]) ]
    
    layers += [ orc.snares(slen, [3*4*8 for i in range(3)], [0,1]) ]
    layers += [ orc.hat(slen, [3*4*8]) ]
    layers += [ orc.hat(slen, [3*4*16]) ]
    layers += [ orc.pat(slen, [3*4, 3*4*2, 3*4*4], [0,0,1]) ]
    layers += [ orc.slicer(orc.bells_rhythm(slen, [1.0, 1.5, 1.667, 2.25]), slen, [3*8*8], [1,0,0]) ]
    layers += [ orc.clicks(slen, [3*4*2, 3*4*3], [0,1,0,1,0,0,1]) ]

    out += dsp.mix(layers)

    ##################
    # C

    slen = dsp.stf(28)

    layers = [ orc.slicer(orc.bells_rhythm(slen, [0.5, 1.0]), slen, [4, 8], [1,0]) ]
    layers += [ orc.slicer(orc.bells_rhythm(slen, [1.888, 2.25]), slen, [4, 8], [1,0]) ]
    layers += [ orc.slicer(orc.bells_rhythm(slen, [2.25, 3.0]), slen, [4, 8], [1,0]) ]
    layers = [dsp.amp(l, 0.5) for l in layers]

    layers += [ orc.melody(slen, [[4.0, 6.0], [3.0, 5.0]], [3, 2], [1]) ]

    layers += [ orc.snares(slen, [2*4*8 for i in range(3)], [0,1]) ]
    layers += [ orc.hat(slen, [2*4*8]) ]
    layers += [ orc.hat(slen, [2*4*16]) ]
    layers += [ orc.pat(slen, [2*4, 2*4*2, 2*4*4], [0,0,1]) ]
    layers += [ orc.slicer(orc.bells_rhythm(slen, [4.0, 1.0, 1.5, 2.25, 3.0]), slen, [2*8*8], [1,0,0]) ]
    layers += [ orc.clicks(slen, [2*4*2, 2*4*3], [0,1,0,1,0,0,1]) ]

    out += dsp.mix(layers)

    out += orc.clicks(dsp.stf(0.25), [1], [1])

    ##################
    # D

    slen = dsp.stf(23)

    layers = [ orc.slicer(orc.bells_rhythm(slen, [0.5, 1.0]), slen, [4, 8], [1,0]) ]
    layers += [ orc.slicer(orc.bells_rhythm(slen, [1.5, 2.25]), slen, [4, 8], [1,0]) ]
    layers += [ orc.slicer(orc.bells_rhythm(slen, [2.25, 3.0]), slen, [4, 8], [1,0]) ]
    layers = [dsp.amp(l, 0.5) for l in layers]

    layers += [ orc.melody(slen, [[4.0, 6.0], [3.0, 5.0]], [3, 2], [1]) ]

    layers += [ orc.snares(slen, [3*4*8 for i in range(3)], [0,1]) ]
    layers += [ orc.hat(slen, [3*4*8]) ]
    layers += [ orc.hat(slen, [3*4*12]) ]
    layers += [ orc.pat(slen, [3*4, 3*4*2, 3*4*4], [0,0,1]) ]
    layers += [ orc.slicer(orc.bells_rhythm(slen, [2.0, 3.0, 1.667, 2.25]), slen, [3*8*8], [1]) ]
    layers += [ orc.clicks(slen, [3*4*2, 3*4*3, 3*8*2], [0,1,0,1,0,0,1]) ]

    out += dsp.mix(layers)

    out += orc.clicks(dsp.stf(0.5), [1], [1])
    out += dsp.pad('', 0, dsp.mstf(100))

    ##################
    # E

    slen = dsp.stf(26)

    layers = [ orc.slicer(orc.bells_rhythm(slen, [0.5, 1.0]), slen, [4, 2], [1,0]) ]
    layers += [ orc.slicer(orc.bells_rhythm(slen, [1.5, 2.5]), slen, [4, 2], [1,0]) ]
    layers += [ orc.slicer(orc.bells_rhythm(slen, [2.5, 3.0]), slen, [4, 2], [1,0]) ]
    layers = [dsp.amp(l, 0.6) for l in layers]

    layers += [ orc.melody(slen, [[4.0, 6.0], [3.0, 5.0]], [3, 2], [1]) ]

    layers += [ orc.snares(slen, [3*2*8 for i in range(3)], [0,1]) ]
    layers += [ orc.hat(slen, [3*2*8]) ]
    layers += [ orc.pat(slen, [3*2, 3*2*2, 3*2*3], [0,0,1,0,0,1,1,0,1]) ]
    layers += [ orc.slicer(orc.bells_rhythm(slen, [3.0, 2.666, 1.667]), slen, [3*4*16], [1,0,0]) ]

    out += dsp.mix(layers)

    ##################
    # F

    slen = dsp.stf(16)

    layers = [ orc.slicer(orc.bells_rhythm(slen, [0.5, 1.0]), slen, [2, 1], [1,0]) ]
    layers += [ orc.slicer(orc.bells_rhythm(slen, [1.5, 2.5]), slen, [2, 1], [1,0]) ]
    layers += [ orc.slicer(orc.bells_rhythm(slen, [2.5, 3.0]), slen, [2, 1], [1,0]) ]
    layers = [dsp.amp(l, 0.6) for l in layers]

    layers += [ orc.melody(slen, [[4.0, 6.0], [3.0, 5.0]], [3, 2], [1]) ]

    layers += [ orc.snares(slen, [3*2*4 for i in range(3)], [0,1]) ]
    layers += [ orc.hat(slen, [3*2*4]) ]
    layers += [ orc.pat(slen, [3, 3*2, 3*3], [0,0,1,0,0,1,1,0,1]) ]
    layers += [ orc.slicer(orc.bells_rhythm(slen, [3.0, 2.666, 1.667]), slen, [3*2*16], [1,0,0]) ]

    out += dsp.mix(layers)

    ##################
    # G
    
    slen = dsp.stf(50)
    orc.tonic = 50.0

    layers = [ orc.slicer(orc.bells_rhythm(slen, [0.5, 1.0]), slen, [4, 2], [1,0]) ]
    layers += [ orc.slicer(orc.bells_rhythm(slen, [1.5, 2.5]), slen, [4, 2], [1,0]) ]
    layers += [ orc.slicer(orc.bells_rhythm(slen, [2.5, 3.0]), slen, [4, 2], [1,0]) ]
    layers = [dsp.amp(l, 0.6) for l in layers]

    layers += [ orc.melody(slen, [[4.0, 6.0], [3.0, 5.0]], [3, 2], [1]) ]

    layers += [ dsp.env(orc.snares(slen, [3*2*8 for i in range(3)], [0,1]), 'phasor') ]
    layers += [ dsp.env(orc.hat(slen, [3*2*8]), 'phasor') ]
    layers += [ orc.pat(slen, [3*2, 3*2*2, 3*2*3], [0,0,1,0,0,1,1,0,1]) ]
    layers += [ orc.slicer(orc.bells_rhythm(slen, [3.0, 2.666, 1.667]), slen, [3*4*16], [1,0,0]) ]

    out += dsp.mix(layers)

    out += orc.clicks(dsp.stf(0.75), [12], [1])

    ###################
    # H

    slen = dsp.stf(100)

    layers = [ orc.slicer(orc.bells_rhythm(slen, [0.5, 1.0, 1.5]), slen, [2], [1]) ]
    layers += [ orc.slicer(orc.bells_rhythm(slen, [1.5, 2.0, 2.25]), slen, [2], [1]) ]
    layers += [ orc.slicer(orc.bells_rhythm(slen, [2.25, 3.0, 4.0]), slen, [2], [1]) ]
    layers += [ orc.pings(dsp.mstf(100), slen, (48 * 2**6, 74 * 2**6)) ]
    layers += [ orc.pings(dsp.mstf(101), slen, (49 * 2**6, 74.5 * 2**6)) ]

    layers += [ orc.melody(slen, [[4.0, 6.0], [3.0, 5.0]], [3, 4], [1,0]) ]
    layers += [ orc.melody(slen, [[4.0, 6.0], [3.0, 5.0]], [3, 2], [0,1]) ]

    out += dsp.mix(layers, True, 0.15)

    out += dsp.env(dsp.amp(dsp.noise(dsp.stf(2)), 0.12), 'line')
    out += orc.clicks(dsp.stf(0.75), [5], [1])
    out += orc.clicks(dsp.stf(0.5), [8], [1])

    out = dsp.write(out, 'pocket', True)
    dsp.timer('stop')

class Orc:
    """ make sound """

    tonic = 75.0

    def melody(self, length, pitches, divisions, pattern, out=''):
        melodies = []
        for division in divisions:
            mlen = int(length / float(division))
            melody = ''
            for i in range(division):
                if pattern[i % len(pattern)] > 0:
                    melody += dsp.env(dsp.mix([self.swells(mlen, p * self.tonic, 'gauss') for p in pitches[i % len(pitches)]]), 'random')
                else:
                    melody += dsp.pad('', 0, mlen)
            melodies += [melody]

        out += dsp.mix(melodies)

        return out
        

    def slicer(self, snd, length, divisions, pattern, out=''):
        slices = []
        for division in divisions:
            slen = int(length / float(division))
            slice = []
            for i in range(division):
                if pattern[i % len(pattern)] == 0:
                    aslice = dsp.pad('', 0, slen)
                else:
                    start = int(i * (dsp.flen(snd) / float(division) - dsp.mstf(100))) + dsp.mstf(dsp.randint(1, 100))
                    clen = int(dsp.rand(slen * 0.75, slen))
                    aslice = dsp.amp(dsp.cut(snd, start + dsp.mstf(100), dsp.mstf(40)), 1.5) + dsp.cut(snd, start, clen)
                    aslice = dsp.pad(dsp.env(aslice, 'phasor'), 0, slen - dsp.flen(aslice))
                    aslice = dsp.amp(aslice, dsp.rand(0.7, 2.0))

                slice.append(aslice)

            slices.append(''.join(slice))

        slices = dsp.mix(slices)
        out += dsp.mix([slices, dsp.amp(dsp.pulsar(slices), 0.45)])

        return out

    def snares(self, length, divisions, pattern, out=''):
        snares = []
        for division in divisions:
            clen = int(length / float(division))
            asnare = range(division)
            for i in range(division):
                snare = dsp.amp(dsp.noise(241), 0.2) + dsp.chirp(dsp.randint(1000, 1010), 9000, 14000, clen - 241, 1, 'phasor')
                asnare[i] = dsp.amp(snare, pattern[i % len(pattern)])

            asnare = ''.join(asnare)
            asnare = dsp.mix([dsp.amp(asnare, 1.1), dsp.pulsar(asnare)])
            snares.append(asnare)

        out += dsp.mix(snares)

        return out

    def clicks(self, length, divisions, pattern, out=''):
        clicks = []
        noise = dsp.noise(length / max(divisions))
        for division in divisions:
            clen = int(length / float(division))
            click = dsp.cut(noise, 0, int(dsp.rand(clen * 0.0125, clen * 0.25)))
            click = [click for i in range(division)]
            for i in range(division):
                if i % len(pattern) == 0:
                    pattern = dsp.rotate(pattern, 1)
                    click[i] = dsp.amp(click[i], pattern[i % len(pattern)])

            clicks.append(''.join([dsp.pad(dsp.env(c, 'random'), 0, clen - dsp.flen(c)) for c in click]))

        out += dsp.amp(dsp.mix(clicks), 0.25)

        return out

    def hat(self, length, divisions, out=''):
        t = dsp.env(dsp.tone(dsp.mstf(20), 11000), 'phasor', True)
        hats = []
        for division in divisions:
            hlen = int(length / float(division))
            hats.append(dsp.pad(t, 0, hlen - dsp.flen(t)) * division)

        out += dsp.amp(dsp.mix(hats), 0.65)

        return out

    def pat(self, length, divisions, pattern, out=''):
        t = dsp.env(dsp.tone(dsp.mstf(60), 10000), 'phasor', True)

        pats = []
        for division in divisions:
            plen = int(length / float(division))
            psublen = int(plen / float(len(pattern)))
            pat = [dsp.env(dsp.tone(dsp.mstf(dsp.randint(20, 100)), dsp.randint(9500, 12000)), 'phasor', True) for i in range(len(pattern))]
            pat = [dsp.randchoose(pat) for i in range(division * len(pattern))]

            for i,p in enumerate(pat):
                if i % len(pattern) == 0:
                    pattern = dsp.rotate(pattern, 1)

                pat[i] = dsp.amp(p, pattern[i % len(pattern)])
           
            pat = [dsp.pad(p, 0, psublen - dsp.flen(p)) for p in pat]
            pats.append(''.join(pat))

        out += dsp.amp(dsp.mix(pats), 0.55)
            

        return out

    def pings(self, grain_size, length, freqs, out=''):
        print 'ping!', grain_size, length, freqs
        tone = dsp.tone(grain_size, freqs[0], 'sine2pi', 0.05)
        tone2 = dsp.tone(grain_size, freqs[1], 'saw', 0.05)
        tone = dsp.mix([tone, tone2])
        out += ''.join([dsp.pulsar(tone, (1.0, 1.05, 'random'), (1.0, 1.0, 'line'), dsp.rand()) for i in range(length / dsp.flen(tone))])
        return out

    def swells(self, length, pitch, env='sine2pi', amp=0.35, fmod=1.01, out=''):
        out += dsp.mix([dsp.pulsar(dsp.tone(length, pitch, env, amp), (1.0, fmod, 'random'), (0.6, 1.0, 'vary'), dsp.rand()) for i in range(3)])
        out = dsp.fill(out, length)
        return out

    def bells_rhythm(self, length, mults=[1.0, 1.5, 1.25], out=''):
        tones = [[dsp.tone(length, self.tonic * m * i, 'sine2pi', 0.2) for i in range(1, 5)] for m in mults]
        tones =  [dsp.mix([dsp.env(t, 'random') for t in tone]) for tone in tones] 
        out += dsp.mix(tones)

        return out

    def bell(self, freq, length, amp):
        bell = dsp.tone(length, freq, 'sine2pi', amp)
        bell = dsp.mix([dsp.pulsar(bell, (1.0, 1.008, 'random'), (0.0, 1.0, 'phasor'), dsp.rand()) for i in range(10)], True, 2.0)

        return bell

      
if __name__ == '__main__':
    main()
