#!/usr/bin/env python2
# -*- coding: UTF-8 -*-

import fabric.fabric as dsp
import random
import time
import audioop 
import math
import subprocess

def main(out=''):
    timer = time.time()

    dsp.snddir = 'sounds/magill_interlude/'
    magill = Magill()
    dsp.beat = dsp.bpm2frames(88.0)

    # Should We All Wake Up
    out += magill.tmp.data

    # prelude
    out += magill.preintroA(magill.ac.data)
    dsp.beat = dsp.bpm2frames(78.0)
    out += magill.guitarphase(magill.ac.data)
    dsp.beat = dsp.bpm2frames(48.0)
    out += magill.preintroB(magill.ac.data)
    dsp.beat = dsp.bpm2frames(28.0)
    out += magill.preintroB(magill.ac.data)
    dsp.beat = dsp.bpm2frames(88.0)

    # Sparkle motion
    intro_b = dsp.mix([magill.introA() for i in range(12)], False, 4.0)
    intro_b += magill.preintroC(magill.ad.data)
    intro_b += dsp.mix([magill.introB() for i in range(12)], True, 4.0)
    out += intro_b

    # Song
    dsp.beat = dsp.bpm2frames(86.0)
    out += magill.song()
    dsp.beat = dsp.bpm2frames(100.0)
    out += magill.preintroC(magill.ad.data)
    out += dsp.env(magill.guitarphase(magill.ad.data), 'phasor')
    #out += magill.guitarphase(magill.ad.data)
    #out += magill.guitarphase(magill.ad.data)
    #out += magill.guitarphase(magill.ad.data)
    #out += magill.guitarphase(magill.ad.data)
    #out += magill.guitarphase(magill.ad.data)
    #out += magill.guitarphase(magill.ad.data)

    out += magill.wesbreak()

    dsp.beat = dsp.bpm2frames(20.0)
    end = dsp.amp(magill.guitarphase(magill.ad.data), 30.0)
    end += dsp.amp(dsp.mix([magill.guitarphase(magill.ad.data), magill.guitarphase(dsp.transpose(magill.ad.data, 0.75))]), 30.0)
    end += dsp.amp(magill.guitarphase(magill.ad.data), 40.0)
    end += dsp.amp(magill.guitarphase(magill.ad.data), 50.0)
    end = dsp.env(end, 'line')
    end += dsp.amp(magill.guitarphase(magill.ad.data), 100.0)
    end = dsp.amp(end, 0.3)
    cap = dsp.cut(end, dsp.flen(end) - dsp.stf(1), dsp.stf(1))

    # Teoh
    end = dsp.mix([dsp.pad(magill.teoh.data, 0, dsp.stf(10)), dsp.mix([dsp.pulsar(end, (1.0, 1.1, 'random')) for i in range(3)], False)], False)
    out += end + cap
    dsp.beat = dsp.bpm2frames(90.0)
    out += magill.preintroC(dsp.transpose(cap, 0.9))

    # All Those I Know
    out += magill.all.data

    out = dsp.write(out, 'magill', False)

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
        self.cara1 = dsp.read('cara_trim01.wav')
        self.cara2 = dsp.read('cara_trim02.wav')

        self.wes1 = dsp.read('wes01n.wav')
        self.wes2 = dsp.read('wes02n.wav')

        self.bren1 = dsp.read('brendan_take01.wav')
        self.bren2 = dsp.read('brendan_take02.wav')
        self.bren3 = dsp.read('brendan_take03.wav')
        self.bren4 = dsp.read('brendan_take04.wav')

        self.ac = dsp.read('wake_end01n.wav')
        self.ad = dsp.read('wake_intro01n.wav')

        #self.tmp = dsp.read('wake_mix_outro.wav')
        self.tmp = dsp.read('wake-mix09.wav')
        self.all = dsp.read('all_those.wav')
        self.test = dsp.read('stereotest.wav')
        self.teoh = dsp.read('teoh.wav')

        # Set audio params
        dsp.audio_params = self.cara2.params

    def guitarphase(self, snd, out=''):
        
        out += dsp.mix([dsp.cut(dsp.transpose(snd, random.random() * 0.01 + 1), random.randint(0, 441 * 40), dsp.stf(5)) for i in range(10)], True, 2.0)

        p = {
            'sounds':[out], 
            'pulse_length_range':(400, 400),
            'pulse_pad': (0, 0),
            'amp_wavetable_type': 'phasor',
            'pan_range': (0.2, 0.8),
            }

        pulseA = [dsp.pulse(dsp.apulse(p, 10), i) for i in range(10)]
        p['amp_wavetable_type'] = 'line'
        pulseB = [dsp.pulse(dsp.apulse(p, 10), i) for i in range(10)]

        p['amp_wavetable_type'] = 'phasor'
        pulseC = [dsp.pulse(dsp.apulse(p, 10), i) for i in range(10)]
        p['amp_wavetable_type'] = 'line'
        pulseD = [dsp.pulse(dsp.apulse(p, 10), i) for i in range(10)]

        pulseA = dsp.mix([''.join(pulseA), ''.join(pulseB)])
        pulseC = dsp.mix([''.join(pulseC), ''.join(pulseD)])

        out = dsp.mix([pulseA, pulseC], True, 1.0)
        out = dsp.env(out, 'phasor')
        out = dsp.mix([out, dsp.env(pulseA, 'line')])
        #out = dsp.cut(out, 0, dsp.stf(17))


        
        return out
        

    def preintroA(self, snd, out=''):
        print '## preintro a'
        out += dsp.cut(snd, dsp.mstf(200), dsp.mstf(20))
        out += dsp.pad('', 0, dsp.mstf(80))
        out += dsp.env(dsp.cut(snd, dsp.mstf(200), dsp.mstf(360)), 'line')

        print '#### preintro a out', dsp.fts(dsp.flen(out))
        print
        return out

    def preintroB(self, snd, out=''):
        out += self.preintroA(snd)
        out = self.slowvoice([out], 1.5, dsp.beat / 10, True, 'sine')
        return out

    def preintroC(self, snd, out=''):
        out = dsp.mix([dsp.env(self.preintroB(snd), 'random') for i in range(4)])
        out = dsp.amp(out, 2.0)
        return out

    def introA(self, snd={}, out=''):
        snd['ad'] = self.ad.data

        print '## intro a'
        out += ''.join(self.patterns.rainbowA(snd))

        dings = [
            self.patterns.dingstreamA(snd, dsp.stf(30), 0.5, 1.0),
            self.patterns.dingstreamA(snd, dsp.stf(30), 1.0, 1.5),
            self.patterns.dingstreamA(snd, dsp.stf(30), 0.75, 2.0),
            self.patterns.dingstreamA(snd, dsp.stf(30), 1.25, 1.0),
            ]
        dings = dsp.env(dsp.mix(dings), 'line')

        out = dsp.mix([out, dings], False, 1.0)

        print '#### intro a out', dsp.fts(dsp.flen(out))
        print
        return out

    def introB(self, snd={}, out=''):
        snd['ad'] = self.ad.data
        print '## intro b'
        
        lifted_voices = {
                'bt2': self.bren2.data,
                'bt3': self.bren3.data,
                'bt4': self.bren4.data,
            }
        lifted = ''.join(self.patterns.lifted(lifted_voices, dsp.stf(120)))
        lifted = dsp.fill(lifted, dsp.stf(120))
        lifted = dsp.env(dsp.amp(lifted, 2.5), 'line')
        print 'lifted len', dsp.fts(dsp.flen(lifted))

        out += dsp.fill(''.join(self.patterns.rainbowB(snd, dsp.stf(40))), dsp.stf(40))
 
        dinggroup = [
            self.patterns.dingstreamA(snd, dsp.stf(40), 0.5, 1.0),
            self.patterns.dingstreamA(snd, dsp.stf(40), 0.33333, 1.5),
            self.patterns.dingstreamA(snd, dsp.stf(40), 0.5, 1.5, 1.2),
            self.patterns.dingstreamA(snd, dsp.stf(40), 0.75, 2.0),
            self.patterns.dingstreamA(snd, dsp.stf(40), 1.25, 1.0, 1.1),
            ]
        dings = dsp.fill(dsp.mix(dinggroup), dsp.stf(20))

        dinggroup = [
            self.patterns.dingstreamA(snd, dsp.stf(40), 0.5, 1.0),
            self.patterns.dingstreamA(snd, dsp.stf(40), 1.0, 0.25),
            self.patterns.dingstreamA(snd, dsp.stf(40), 1.0, 0.5),
            self.patterns.dingstreamA(snd, dsp.stf(40), 0.3333333, 2.0),
            self.patterns.dingstreamA(snd, dsp.stf(40), 1.25, 1.0, 1.1),
            ]
        dings += dsp.fill(dsp.mix(dinggroup), dsp.stf(40))

        dingswell = dsp.amp(dsp.env(dsp.fill(self.patterns.dingstreamA(snd, dsp.stf(60), 0.5, 3.333333333333, 1.02), dsp.stf(60))), 0.55)
        out = dsp.mix([out, dings, dingswell], False, 1.5)   

        dinggroup = [
            self.patterns.dingstreamA(snd, dsp.stf(60), 0.5, 1.0),
            self.patterns.dingstreamA(snd, dsp.stf(60), 1.5, 0.5),
            self.patterns.dingstreamA(snd, dsp.stf(60), 1.0, 0.5),
            self.patterns.dingstreamA(snd, dsp.stf(60), 0.75, 2.0),
            self.patterns.dingstreamA(snd, dsp.stf(60), 1.25, 1.0),
            ]
        dings = dsp.mix(dinggroup)
        dings = dsp.fill(dings, dsp.stf(60))
        dingswell = dsp.amp(dsp.env(dsp.fill(dsp.mix([self.patterns.dingstreamA(snd, dsp.stf(60), 0.3333333, 8.0, 2.0), dingswell]), dsp.stf(60))), 0.6)
        out += dsp.mix([out, dings, dingswell], False, 1.5)   

        out = dsp.mix([out, lifted], False)

        print '#### intro b out', dsp.fts(dsp.flen(out))
        print
        return out

    def introC(self, snd={}, out=''):
        snd['ad'] = self.ad.data
        print '## intro c'

        out += dsp.fill(''.join(self.patterns.rainbowB(snd, dsp.stf(60))), dsp.stf(60))
        out = dsp.amp(out, 0.4)

        phrase_len = dsp.stf(10)
 
        dinggroup = [
            self.patterns.dingstreamA(snd, phrase_len, 0.5, 1.0),
            self.patterns.dingstreamA(snd, phrase_len, 0.33333, 0.75),
            self.patterns.dingstreamA(snd, phrase_len, 0.5, 1.25, 1.2),
            self.patterns.dingstreamA(snd, phrase_len, 0.75, 0.5),
            self.patterns.dingstreamA(snd, phrase_len, 1.25, 1.0, 1.1),
            ]
        dings = dsp.mix(dinggroup, False)

        dinggroup = [
            self.patterns.dingstreamA(snd, phrase_len, 0.5, 1.0),
            self.patterns.dingstreamA(snd, phrase_len, 0.33333, 0.5),
            self.patterns.dingstreamA(snd, phrase_len, 0.5, 1.5, 1.2),
            self.patterns.dingstreamA(snd, phrase_len, 0.75, 0.5),
            self.patterns.dingstreamA(snd, phrase_len, 1.25, 1.0, 1.1),
            ]
        dings += dsp.mix(dinggroup, False)

        out = dsp.mix([out, dings], False, 1.5)   

        print '#### intro c out', dsp.fts(dsp.flen(out))
        print

        return out

    def wesbreak(self, p={}, out=''):
        dsp.beat = dsp.bpm2frames(84.0 * 2)
        w1 = self.wes1.data
        w2 = self.wes2.data

        wa = dsp.cut(w1, dsp.stf(42), dsp.stf(4))
        wb = dsp.cut(w1, dsp.stf(69), dsp.stf(4))

        wc = dsp.cut(w2, dsp.stf(32), dsp.stf(4))
        wd = dsp.cut(w2, dsp.stf(45.5), dsp.stf(3.5))
        we = dsp.cut(w2, dsp.stf(57), dsp.stf(4))
        wf = dsp.cut(w2, dsp.stf(61), dsp.stf(8))

        #wes = dsp.amp(dsp.mix([wa, wb, wd, we, wf]), 2.0)
        #wesd = dsp.amp(wes, 100.0)
        #wesd = dsp.amp(wesd, 0.04)
        #wes = dsp.mix([wes, wesd])

        we_parts = dsp.interleave(dsp.split(we, dsp.mstf(60)), dsp.split(wd, dsp.mstf(70)))
        we_freq = (0.9, 1.05, 'random')
        we_amp = (0.0, 1.0, 'sine')
        enough_rise = dsp.mix([''.join([dsp.pad(dsp.pulsar(we_part, we_freq, we_amp, random.random()), 0, random.randint(20, 1000)) for we_part in we_parts]) for i in range(40)], False, 8.0)
        out += enough_rise

        we_parts = dsp.interleave(dsp.split(we, dsp.mstf(100)), dsp.split(wd, dsp.mstf(120)))
        we_freq = (0.8, 1.0, 'random')
        enough_rise = dsp.mix([''.join([dsp.pad(dsp.pulsar(we_part, we_freq, we_amp, random.random()), 0, random.randint(200, 2000)) for we_part in we_parts]) for i in range(40)], False, 8.0)
        out += enough_rise

        we_parts = dsp.interleave(dsp.split(wf, dsp.mstf(70)), dsp.split(wf, dsp.mstf(200)))
        we_freq = (0.8, 1.0, 'random')
        enough_enough = dsp.mix([''.join([dsp.pad(dsp.pulsar(we_part, we_freq, we_amp, random.random()), 0, random.randint(20, 200)) for we_part in we_parts]) for i in range(40)], False, 8.0)

        we_freq = (0.9, 1.05, 'random')
        enough_smudge = dsp.mix([dsp.pulsar(random.choice([wd, we]), (1.0, 1.07, 'random'), (0.0, 1.0, 'random'), random.random()) for i in range(40)], True, 8)
        enough_smudgy = dsp.mix([dsp.pulsar(random.choice([wd, we]), (1.0, 1.07, 'random'), (0.0, 1.0, 'random'), random.random()) for i in range(40)], True, 8)
        out += dsp.mix([enough_smudge, enough_smudgy, enough_enough])

        #out += dsp.mix([ga, dsp.amp(gb, 0.1)], False)
        #out += wes

        #out += dsp.pad('', dsp.mstf(100), dsp.stf(0))
        #out += wa # that should be enough
        #out += dsp.pad('', dsp.mstf(100), dsp.stf(0))
        #out += wb # enouuuugh
        #out += dsp.pad('', dsp.mstf(100), dsp.stf(0))
        #out += wc # blast over accordingly

        #out += dsp.pad('', dsp.mstf(100), dsp.stf(0))
        #out += wd # that should be mid
        #out += dsp.pad('', dsp.mstf(100), dsp.stf(0))
        #out += we # that should be high

        out += dsp.pad('', dsp.mstf(1000), dsp.stf(0))
        #out += wf


        return out



    def song(self, p={}, out=''):
        p['voicespeed'] = 3
        p['voicebeat'] = dsp.beat / 4
        p['voicelayers'] = 4

        c = dsp.mix([self.cara1.data, self.cara2.data])
        b = dsp.mix([self.bren2.data, self.bren4.data])

        w1 = self.wes1.data
        w2 = self.wes2.data

        w_chorus_a = dsp.cut(w1, dsp.stf(42), dsp.stf(4))
        w_chorus_b = dsp.cut(w1, dsp.stf(69), dsp.stf(4))

        w_chorus_c = dsp.cut(w2, dsp.stf(32), dsp.stf(4))
        w_chorus_d = dsp.cut(w2, dsp.stf(45.5), dsp.stf(3.5))
        w_chorus_e = dsp.cut(w2, dsp.stf(57), dsp.stf(4))
        w_chorus_f = dsp.cut(w2, dsp.stf(61), dsp.stf(7))

        c_verse_a = dsp.cut(c, 0, dsp.stf(2.5))
        b_verse_a = dsp.cut(b, 0, dsp.stf(2.5))

        c_verse_b = dsp.cut(c, dsp.stf(4), dsp.stf(3))
        b_verse_b = dsp.cut(b, dsp.stf(4), dsp.stf(3))

        c_verse_c = dsp.cut(c, dsp.stf(8), dsp.stf(3))
        b_verse_c = dsp.cut(b, dsp.stf(8.5), dsp.stf(2.5))

        c_verse_d = dsp.cut(c, dsp.stf(11.5), dsp.stf(3))
        b_verse_d = dsp.cut(b, dsp.stf(12), dsp.stf(3))

        c_verse_e = dsp.cut(c, dsp.stf(15), dsp.stf(2))
        b_verse_e = dsp.cut(b, dsp.stf(16), dsp.stf(2))

        c_verse_f = dsp.cut(c, dsp.stf(19), dsp.stf(3))
        b_verse_f = dsp.cut(b, dsp.stf(20), dsp.stf(3))

        c_verse_g = dsp.cut(c, dsp.stf(23.5), dsp.stf(4.5))
        b_verse_g = dsp.cut(b, dsp.stf(24), dsp.stf(5))

        c_chorus_a = dsp.cut(c, dsp.stf(29.5), dsp.stf(4.0))
        b_chorus_a = dsp.cut(b, dsp.stf(29.5), dsp.stf(4.0))

        c_chorus_b = dsp.cut(c, dsp.stf(34.5), dsp.stf(7.0))
        b_chorus_b = dsp.cut(b, dsp.stf(34.5), dsp.stf(7.0))

        c_chorus_c = dsp.cut(c, dsp.stf(37), dsp.stf(3.5))
        b_chorus_c = dsp.cut(b, dsp.stf(37), dsp.stf(3.5))

        g1 = dsp.cut(self.ad.data, 0, dsp.stf(5))
        g2 = dsp.fill(dsp.transpose(g1, 2.0), dsp.stf(5))
        g3 = dsp.fill(dsp.transpose(g1, 0.5), dsp.stf(5))
        g4 = dsp.fill(dsp.transpose(g1, 0.25), dsp.stf(5))
        g5 = dsp.fill(dsp.transpose(g1, 4.0), dsp.stf(5))

        # ding lead
        p['voicerand'] = True
        p['voices'] = [dsp.pad('', dsp.stf(3), 0)]
        p['guitars'] = ([g1, g2], [g1, g2, g3])
        out += self.sing(p)

        ## oh greedy eyes
        p['voicespeed'] = 1.5 
        p['voices'] = [b_verse_a, c_verse_a]
        p['guitars'] = ([g4], [g3])
        out += self.sing(p)

        dsp.beat = dsp.bpm2frames(84.0)
        out += self.preintroC(g4)
        out += self.preintroC(g4)

        # would you find
        dsp.beat = dsp.bpm2frames(88.0)
        p['voicespeed'] = 1.5 
        p['voices'] = [b_verse_b, c_verse_b]
        p['guitars'] = ([g2, g4], [g1, g2])
        out += self.sing(p)

        # not lifted 
        dsp.beat = dsp.bpm2frames(88.0 * 2.5)
        out += self.preintroC(g5)
        p['voicespeed'] = 0.7 
        p['voices'] = [b_verse_d, c_verse_d]
        p['guitars'] = ([g2, g4], [g2, g3])
        out += self.sing(p)

        # you find some
        p['voicespeed'] = 0.5 
        p['voices'] = [b_verse_e, c_verse_e]
        p['guitars'] = ([g1, g2, g4], [g1, g2, g3])
        dsp.beat = dsp.bpm2frames(88.0 * 4.5)
        out += self.preintroC(g2)
        dsp.beat = dsp.bpm2frames(88.0 * 5)
        out += self.preintroC(g4)
        out += self.preintroC(g4)
        dsp.beat = dsp.bpm2frames(88.0 * 3)
        out += self.preintroC(g4)
        dsp.beat = dsp.bpm2frames(88.0 * 1.5)
        out += self.preintroC(g4)
        out += self.preintroC(g4)
        dsp.beat = dsp.bpm2frames(88.0 * 0.75)
        out += self.preintroC(g4)
        dsp.beat = dsp.bpm2frames(20.0)
        out += self.preintroC(g4)
        
        ## lifted in the air
        dsp.beat = dsp.bpm2frames(88.0)
        p['voicerand'] = False 
        p['voicespeed'] = 4.5
        p['voices'] = [b_verse_g, c_verse_g]
        p['guitars'] = ([g5], [g2])
        out += self.sing(p)

        out += self.preintroC(self.ad.data)
        out += self.preintroC(dsp.transpose(g5, 0.5))

        # should we all wake up
        dsp.beat = dsp.bpm2frames(84.0)
        p['voicespeed'] = 2.6
        p['voices'] = [dsp.amp(b_chorus_a, 0.9), dsp.amp(c_chorus_a, 0.4)]
        p['guitars'] = ([g1], [g1, g3])
        big = self.sing(p)

        snd = {'ad': self.ad.data }
        dinggroup = [
            self.patterns.dingstreamA(snd, dsp.flen(big), 0.5, 2.667),
            self.patterns.dingstreamA(snd, dsp.flen(big), 0.33333, 2.667),
            self.patterns.dingstreamA(snd, dsp.flen(big), 0.5, 2.667, 1.2),
            self.patterns.dingstreamA(snd, dsp.flen(big), 0.75, 2.667),
            self.patterns.dingstreamA(snd, dsp.flen(big), 1.25, 2.667, 1.1),
            ]
        dings = dsp.fill(dsp.mix(dinggroup), dsp.flen(big))

        numhats = dsp.flen(big) / dsp.beat
        hat = dsp.cut(self.ad.data, 0, dsp.mstf(60))
        nohat = dsp.pad('', dsp.mstf(60), 0)
        hats = [dsp.pad(dsp.pulsar(random.choice([hat, nohat])), 0, dsp.beat - dsp.mstf(60)) for i in range(numhats)]
        hats = ''.join(hats)

        numhats = dsp.flen(big) / (dsp.beat / 3)
        hat = dsp.alias(dsp.cut(self.ad.data, 0, dsp.mstf(30)))
        nohat = dsp.pad('', dsp.mstf(30), 0)
        hatz = [dsp.pad(dsp.pulsar(random.choice([dsp.alias(hat), nohat])), 0, (dsp.beat / 3) - dsp.mstf(30)) for i in range(numhats)]
        hats = dsp.mix([dsp.amp(''.join(hatz), 1.2), hats])

        out += dsp.mix([hats, big, dsp.amp(dings, 0.5)])

        # dings
        p['voicerand'] = True
        p['voicespeed'] = 1.0
        p['guitars'] = ([g5], [g2])
        p['voices'] = [dsp.pad('', dsp.stf(2), 0)]
        out += self.sing(p)

        # should we all wake up
        dsp.beat = dsp.bpm2frames(90.0)
        p['voicerand'] = False 
        p['voicespeed'] = 3.6
        p['voices'] = [dsp.amp(b_chorus_c, 1.2), dsp.amp(c_chorus_c, 0.8)]
        p['guitars'] = ([g1], [g3])
        big = self.sing(p)

        dinggroup = [
            self.patterns.dingstreamA(snd, dsp.flen(big), 0.5, 2.667 * 2),
            self.patterns.dingstreamA(snd, dsp.flen(big), 0.33333, 2.667 * 2),
            self.patterns.dingstreamA(snd, dsp.flen(big), 0.5, 2.667, 1.2),
            self.patterns.dingstreamA(snd, dsp.flen(big), 0.75, 2.667),
            self.patterns.dingstreamA(snd, dsp.flen(big), 1.25, 2.667, 1.1),
            ]
        dings = dsp.fill(dsp.mix(dinggroup), dsp.flen(big))

        out += dsp.mix([big, dsp.amp(dings, 0.5)])

        return out

    def sing(self, p, out=''):

        out += dsp.mix([dsp.mix([self.slowvoice(p['voices'], p['voicespeed'], p['voicebeat'], p['voicerand'], 'line'), self.slowvoice(p['voices'], p['voicespeed'], p['voicebeat'], p['voicerand'])]) for i in range(p['voicelayers'])])
        out = dsp.amp(out, 1.8)

        guitarspeed = dsp.flen(out) / float(dsp.stf(5))
        guitars = dsp.mix([self.slowvoice(p['guitars'][0], guitarspeed, (dsp.beat / 4) * 2, True, 'phasor'), self.slowvoice(p['guitars'][1], guitarspeed, (dsp.beat / 3), True, 'phasor')])
        guitars = dsp.amp(guitars, 0.7)

        out = dsp.mix([out, guitars])

        print 'sing len', dsp.fts(dsp.flen(out))

        return out
        
 
    def slowvoice(self, sounds, speed, beat, vary=False, envtype='random', out=''): 
        sounds.sort(key = len)
        goal_len = int(speed * dsp.flen(sounds[-1]))
        num_pulses = goal_len / beat 
        num_steps = num_pulses / 10 
        if num_steps < 2:
            num_steps = 2

        print 'slow voice', dsp.ftms(beat), num_pulses, num_steps, dsp.fts(goal_len), dsp.fts(dsp.flen(sounds[-1]))

        pan_values = [random.random() for i in range(num_steps)]
        len_values = [random.random() for i in range(num_steps)]
        if vary == True:
            pos_values = [random.random() for i in range(num_steps)]
        elif vary == False:
            pos_values = [i / float(num_steps) for i in range(num_steps)]
        freq_values = [random.random() for i in range(num_steps)]
   
        params = {
            'sounds': sounds,
            'amp_wavetable_type': envtype,
            'freq_wavetable_type': 'random',

            'pan_table': dsp.breakpoint(pan_values, num_pulses),
            'pan_range': (0.0,1.0), # 0 is left, 1 is right

            'pulse_length_range': (dsp.ftms(beat), dsp.ftms(beat)), 
            'pulse_length_table': dsp.breakpoint(len_values, num_pulses),

            'pulse_pad': (0, 0),

            'freq_width_range': (0.0, 0.004), 
            'freq_width_table': dsp.breakpoint(freq_values, num_pulses),

            'pos_range': (0.0, 1.0),
            'pos_table': dsp.breakpoint(pos_values, num_pulses),
        }

        smear = ''.join([dsp.pulse(params, i) for i in range(num_pulses)])

        out = dsp.amp(smear, 0.8)
        return out

class Patterns:
    """ recipes, patterns """

    def lifted(self, snd, length):
        sounds = [
            dsp.cut(snd['bt2'], dsp.stf(24), dsp.stf(4)),
            dsp.cut(snd['bt3'], dsp.stf(25), dsp.stf(4)),
            dsp.cut(snd['bt4'], dsp.stf(25), dsp.stf(4)),
        ]
 
        pulse_length_min = 8 
        pulse_length_max = 300 
        pulse_pad_min = 0
        pulse_pad_max = 40 

        num_pulses = length / (dsp.mstf(pulse_length_max) + dsp.mstf(pulse_pad_max)) 

        print 'lifted!', num_pulses

        #pan_values = [random.random() for i in range(4)]
        pan_values = [0.0, 1.0, 0.0, 1.0, 0.0, 1.0, 0.0, 1.0, 0.2, 1.0, 0.0, 1.0, 0.0, 1.0, 0.0, 1.0, 0.0, 0.5]
        len_values = [0.7, 0.3, 0.1, 0.35, 1.0]
        pos_values = [0.0, 0.1, 0.15, 0.5, 0.7, 0.8, 0.85, 0.9, 0.95, 1.0]
        freq_values = [1.0, 0.8, 0.9, 1.0, 0.7, 0.8, 0.85, 0.6, 0.9, 0.8, 0.55, 0.0]

        params = {
                'sounds': sounds,
                'amp_wavetable_type': 'random',
                'freq_wavetable_type': 'random',

                'pan_table': dsp.breakpoint(pan_values, num_pulses),
                'pan_range': (0.0,1.0), # 0 is left, 1 is right

                'pulse_length_range': (pulse_length_min, pulse_length_max), 
                'pulse_length_table': dsp.breakpoint(len_values, num_pulses),

                'pulse_pad': (pulse_pad_min, pulse_pad_max),

                'freq_width_range': (0.0, 0.001), 
                'freq_width_table': dsp.breakpoint(freq_values, num_pulses),

                'pos_range': (0.0, 1.0),
                'pos_table': dsp.breakpoint(pos_values, num_pulses),
        }

        pulses = [dsp.pulse(params, i) for i in range(num_pulses)]

        return pulses

    def rainbowA(self, snd):
        num_pulses = 48 * 2 

        print 'rainbow!', num_pulses

        pulses = []

        pan_values = [random.random() for i in range(4)]
        
        len_values = [0.0, 0.01, 0.1, 0.35, 1.0]

        pos_values = [random.random() for i in range(4)]

        freq_values = [1.0, 0.8, 0.9, 1.0, 0.7, 0.8, 0.85, 0.6, 0.9, 0.8, 0.55, 0.0]

        params = {
                'sounds': [snd['ad']],
                'amp_wavetable_type': 'random',
                'freq_wavetable_type': 'random',

                'pan_table': dsp.breakpoint(pan_values, num_pulses),
                'pan_range': (0.0,1.0), # 0 is left, 1 is right

                'pulse_length_range': (100, 400), 
                'pulse_length_table': dsp.breakpoint(len_values, num_pulses),

                'pulse_pad': (0.0, 0.0),

                'freq_width_range': (0.0, 0.0), 
                'freq_width_table': dsp.breakpoint(freq_values, num_pulses),

                'pos_range': (0.0, 1.0),
                'pos_table': dsp.breakpoint(pos_values, num_pulses),
        }

        pulses.extend([dsp.pulse(params, i) for i in range(num_pulses)])

        params['pulse_length_range'] = (320, 560)
        len_values = [0.7, 0.3, 0.1, 0.35, 1.0]
        params['freq_width_range'] = (0.0, 0.001)
        pulses.extend([dsp.pulse(params, i) for i in range(num_pulses)])

        return pulses

    def rainbowB(self, snd, length):

        pulse_length_min = 420 
        pulse_length_max = 520 
        pulse_pad_min = 0
        pulse_pad_max = 0

        num_pulses = length / (dsp.mstf(pulse_length_max) + dsp.mstf(pulse_pad_max)) 

        print 'rainbow!', num_pulses

        pan_values = [random.random() for i in range(4)]
        len_values = [0.7, 0.3, 0.1, 0.35, 1.0]
        pos_values = [random.random() for i in range(4)]
        freq_values = [1.0, 0.8, 0.9, 1.0, 0.7, 0.8, 0.85, 0.6, 0.9, 0.8, 0.55, 0.0]

        params = {
                'sounds': [snd['ad']],
                'amp_wavetable_type': 'random',
                'freq_wavetable_type': 'random',

                'pan_table': dsp.breakpoint(pan_values, num_pulses),
                'pan_range': (0.0,1.0), # 0 is left, 1 is right

                'pulse_length_range': (pulse_length_min, pulse_length_max), 
                'pulse_length_table': dsp.breakpoint(len_values, num_pulses),

                'pulse_pad': (pulse_pad_min, pulse_pad_max),

                'freq_width_range': (0.0, 0.001), 
                'freq_width_table': dsp.breakpoint(freq_values, num_pulses),

                'pos_range': (0.0, 1.0),
                'pos_table': dsp.breakpoint(pos_values, num_pulses),
        }

        pulses = [dsp.pulse(params, i) for i in range(num_pulses)]

        return pulses

    def dingstreamA(self, snd, length, bmult=1.0, fmult=1.0, bdrift=1.01):
        print 'ding!', dsp.fts(length), bmult, fmult

        low = dsp.transpose(snd['ad'], 0.75 * fmult)
        mid = dsp.transpose(snd['ad'], 1.0 * fmult)
        high  = dsp.transpose(snd['ad'], 1.5 * fmult)
        
        pulse_length_min = dsp.ftms(dsp.beat) * bmult
        pulse_length_max = dsp.ftms(dsp.beat * bdrift) * bmult
        pulse_pad_min = 0
        pulse_pad_max = dsp.flen(high) / 20

        num_pulses = length / (dsp.mstf(pulse_length_min) + dsp.mstf(pulse_pad_min)) 
        print 'numpulses', num_pulses
        pulses = []

        pan_values = [random.random() for i in range(4)]
        pan_table = dsp.breakpoint(pan_values, num_pulses)

        len_values = [0.0, 0.5, 0.25, 0.75, 1.0, 0.0]
        pos_values = [random.random() for i in range(4)]
        freq_values = [0.9, 1.0, 0.6, 0.9, 0.55, 0.0]

        params = {
                'sounds': [low, mid, high],
                'amp_wavetable_type': 'random',
                'freq_wavetable_type': 'random',

                'pan_table': pan_table,
                'pan_range': (0.0,1.0), # 0 is left, 1 is right

                'pulse_length_range': (pulse_length_min, pulse_length_max), 
                'pulse_length_table': dsp.breakpoint(len_values, num_pulses),

                'pulse_pad': (pulse_pad_min, pulse_pad_max),

                'freq_width_range': (0.0, 0.001), 
                'freq_width_table': dsp.breakpoint(freq_values, num_pulses),

                'pos_range': (0.0, 0.015),
                'pos_table': dsp.breakpoint(pos_values, num_pulses),
        }

        pulses.extend([dsp.pulse(params, i) for i in range(num_pulses)])

        pulses = ''.join(pulses)
        print 'pulse length:', dsp.fts(dsp.flen(pulses))

        return pulses


      
if __name__ == '__main__':
    main()
