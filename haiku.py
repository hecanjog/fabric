import dsp

dsp.timer('start')

class Orc:
    snds = [
            dsp.read('sounds/dig1.wav').data,
            dsp.read('sounds/dig2.wav').data,
            dsp.read('sounds/dig3.wav').data,
            dsp.read('sounds/dig4.wav').data,
            dsp.read('sounds/dig5.wav').data,
           ]

    scale = [
                1.0 / 1.0,
                16.0 / 15.0,
                10.0 / 9.0,
                6.0 / 5.0,
                5.0 / 4.0,
                4.0 / 3.0,
                64.0 / 45.0,
                3.0 / 2.0,
                8.0 / 5.0,
                27.0 / 16.0,
                16.0 / 9.0,
                15.0 / 8.0,
            ]

    def pop(self, x=0.5, r=3.765, i=30):
        out = []
        for t in range(i):
            x = r * x * (1.0 - x)
            out += [ x ]

        return out 

    def mirror(self, l):
        a = l[:len(l)/2 + 1]
        b = a[:]
        b.reverse()
        t = len(l)
        l = a + b

        if len(l) > t:
            return l[:t]   

        return l

    def train(self, snd, seed, length, hz):
        pitches = [ self.scale[p - 1] for p in [1,3,5,7,5,3,1] ]

        num = int(length / dsp.htf(hz))

        amp = self.mirror(self.pop(seed * 0.5, 3.8, num))
        speed = self.mirror([ 7.0 / pitches[int(s * 7)] for s in self.pop(seed * 0.125, 3.8, num) ])
        width = self.mirror(dsp.wavetable('random', num)) # Okay, one 'random' part! So it goes.
        pan = self.mirror(self.pop(seed * 0.75, 3.8, num))
        pos = [ int((dsp.flen(snd) - hz) * s) for s in dsp.wavetable('line', num) ]

        return ''.join([ self.impulse(snd, amp[i], speed[i], width[i], pan[i], pos[i], hz) for i in range(num) ])

    def impulse(self, snd, amp, speed, width, pan, pos, hz):
        target = hz
        hz = int(hz * (1.0 / speed))
        width = int(hz * width)

        snd = dsp.cut(snd, pos, hz)
        snd = dsp.amp(snd, amp)
        snd = dsp.pan(snd, pan)
        snd = dsp.transpose(snd, speed)
        snd = dsp.cut(snd, 0, width)
        snd = dsp.env(snd, 'sine', True)
        snd = dsp.pad(snd, 0, hz - width)

        return snd

orc = Orc()

def seq(num, seedseed):
    seed = orc.pop(seedseed, 3.9, num)
    length = [ dsp.stf(5) * p + dsp.mstf(10) for p in orc.pop(seedseed * 0.8, 3.85, num) ]
    hz = [ 1100 * p + 1 for p in orc.pop(seedseed * 0.3, 3.8, num) ]

    return ''.join([ orc.train(orc.snds[i % 5], seed[i], length[i], hz[i]) for i in range(num) ])

out = dsp.mix([seq(40, (i + 1) / 4.0) for i in range(4)], False, 3.0)
     
print dsp.write(out, 'palindrone')
dsp.timer('stop')
