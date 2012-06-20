import dsp
import math

dsp.timer('start')

class Orc:
    cpop = 0.444

    def pop(self, i=30):
        x = self.rpop(0.1, 0.9)
        r = self.rpop(3.765, 3.9)
        out = []
        for t in range(i):
            x = r * x * (1.0 - x)
            out += [ x ]

        return out 

    def rpop(self, low, high):
        self.cpop = 3.77 * self.cpop * (1.0 - self.cpop)
        
        return self.cpop * (high - low) + low

    def train(self, length, hz):
        num = int(length / dsp.htf(hz))

        print dsp.fts(length), hz

        amp = self.pop(num)
        wtables = ['gauss', 'line', 'phasor'] + ['vary' for v in range(12)]
        width = dsp.wavetable(wtables[int(self.rpop(0, 14))], num, self.rpop(0.0, 2.5), self.rpop(2.5, 5.0), self.rpop) # Not random anymore, yay!
        pan = self.pop(num)

        return ''.join([ self.impulse(amp[i], width[i], pan[i], hz) for i in range(num) ])

    def impulse(self, amp, width, pan, hz):
        width = int(dsp.htf(hz) * math.fabs(width))

        snd = dsp.cycle(dsp.fth(width))
        snd = dsp.amp(snd, amp)
        snd = dsp.pan(snd, pan)
        snd = dsp.pad(snd, 0, dsp.htf(hz) - dsp.flen(snd))

        return snd

orc = Orc()

def seq(num):
    length = [ dsp.mstf(orc.rpop(300, 3000)) * p + dsp.mstf(orc.rpop(1, 300)) for p in orc.pop(num) ]
    hz = [ orc.rpop(200, 1000) * p + orc.rpop(1, 200) for p in orc.pop(num) ]

    return ''.join([ orc.train(length[i], hz[i]) for i in range(num) ])

out = dsp.mix([seq(40) for o in range(2)], False)
     
print dsp.write(out, 'popopop')
dsp.timer('stop')
