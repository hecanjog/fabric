#!/usr/bin/env python2
# -*- coding: UTF-8 -*-

import fabric.fabric as dsp

def main(out='', layers=[]):
    """ sending dreams to she downstream """
    dsp.timer('start')
    dsp.seed('pocket')

    dsp.snddir = 'sounds/'
    orc = Orc()

    #layers = [ orc.pings(dsp.mstf(100), dsp.stf(40), (50 * 2**6, 75 * 2**6)) ]
    #layers.append(orc.pings(dsp.mstf(101), dsp.stf(40), (50 * 2**6, 75 * 2**6)))
    #layers = [dsp.env(dsp.mix(layers), 'line')] # Mix and envelope pings down to layer 0 
    #layers.append(orc.opening(dsp.stf(200)))
    #layers.append(orc.bells_prelude() + orc.bells_opening())
    #out += dsp.mix(layers, False)


    #slen = dsp.stf(30)
    #layers =  [ orc.clicks(slen, [3*2, 3], [1]) ]
    #layers += [ dsp.env(orc.hat(slen, [6*2*6]), 'line') ]
    #layers += [ dsp.env(orc.pat(slen, [3*2], [0,0,1,0,0,1,1,0,1])) ]

    #layers += [ orc.slicer(bells, slen, [3*4, 3*6, 3, 3*8], [1]) ]
    
    #layers += [ orc.pings(dsp.mstf(100), slen, (50 * 2**6, 80 * 2**6)) ]
    #layers += [ orc.pings(dsp.mstf(101), slen, (50 * 2**6, 80 * 2**6)) ]

    #out += dsp.mix(layers)

    slen = dsp.stf(40)
    layers =  [ orc.snares(slen, [3*4*8 for i in range(3)], [0,1]) ]
    layers += [ orc.hat(slen, [3*4*8]) ]
    layers += [ orc.pat(slen, [3*4, 3*4*2, 3*4*3], [0,0,1,0,0,1,1,0,1]) ]
    layers += [ orc.slicer(orc.bells_rhythm(slen), slen, [3*8*16], [1,0,0]) ]
    out += dsp.mix(layers)

    slen = dsp.stf(43)
    layers =  [ orc.snares(slen, [3*4*8 for i in range(3)], [0,1]) ]
    layers += [ orc.hat(slen, [3*4*8]) ]
    layers += [ orc.pat(slen, [3*4, 3*4*2, 3*4*4], [0,0,1]) ]
    layers += [ orc.slicer(orc.bells_rhythm(slen), slen, [3*8*8], [1,0,0]) ]
    layers += [ orc.clicks(slen, [3*4*2, 3*4*3], [0,1,0,1,0,0,1]) ]
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
                    clen = int(dsp.rand(slen * 0.5, slen))
                    aslice = dsp.amp(dsp.cut(snd, start + dsp.mstf(100), dsp.mstf(40)), 1.5) + dsp.cut(snd, start, clen)
                    aslice = dsp.pad(dsp.env(aslice, 'random'), 0, slen - dsp.flen(aslice))
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

        out += dsp.mix(hats)

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

        out += dsp.amp(dsp.mix(pats), 0.75)
            

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

    def bells_prelude(self, out=''):
        out += self.bell_stream([(75, dsp.stf(10), 0.4)])
        out += self.bell_stream([(75, dsp.stf(11), 0.4)])
        out += self.bell_stream([(75, dsp.stf(12), 0.4)])
        out += self.bell_stream([(75, dsp.stf(14), 0.5)])

        return out

    def bells_rhythm(self, length, out=''):
        tones =  [dsp.tone(length, 75 * i, 'sine2pi', 0.1) for i in range(1, 9)]
        tones += [dsp.tone(length, 75 * 1.5 * i, 'sine2pi', 0.2) for i in range(1, 5)]
        tones += [dsp.tone(length, 75 * 1.25 * i, 'sine2pi', 0.2) for i in range(1, 5)]
        tones =  [dsp.env(t, 'random') for t in tones]

        out += dsp.mix(tones)

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
