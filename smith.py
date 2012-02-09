import fabric.fabric as dsp

def main(out=''):
    dsp.timer('start') 
    dsp.snddir = 'sounds/smith/'
    dsp.seed = 'smith'
    dsp.beat = 29400 # in frames

    orc = Orc()

    layers =  [ orc.mess() ]
    layers += [ orc.beats() ]
    layers += [ orc.swells() ]
    out += dsp.mix(layers)

    print dsp.write(out, 'smith-all', False)

    print dsp.write(layers[0], 'smith-mess', False)
    print dsp.write(layers[1], 'smith-pianos', False)
    print dsp.write(layers[2], 'smith-beats', False)
    print dsp.write(orc.elf(), 'smith-elf', False)

    dsp.timer('stop')

class Orc:
    def __init__(self):
        self.master = dsp.read('master.wav')
        self.drums = dsp.read('drums.wav')
        self.piano = dsp.read('piano.wav')
        self.summer = dsp.read('summer.wav')

    def elf(self, out=''):
        self.summer.data = dsp.transpose(self.summer.data, 1.058)
        f = dsp.htf(2)
        ntimes = dsp.flen(self.summer.data) / 10000 
        starts = dsp.wavetable('line', ntimes)
        clen = dsp.flen(self.summer.data) - f 

        etypes = ['line', 'phasor', 'sine', 'cos', 'tri', 'saw', 'flat']

        cycles = [dsp.panenv(dsp.cut(self.summer.data, starts[i] * clen, f), dsp.randchoose(etypes), 'gauss') for i in range(ntimes)]
        layers = [ ''.join(cycles) ]

        f = dsp.htf(2.1)
        cycles = [dsp.panenv(dsp.cut(self.summer.data, starts[i] * clen, f), dsp.randchoose(etypes), 'sine') for i in range(ntimes)]
        layers += [ ''.join(cycles) ]

        out += dsp.mix(layers, True, 0.9)

        return out


    def swells(self, out=''):
        parts = dsp.split(self.piano.data, dsp.beat)

        layers = [ ''.join([dsp.env(dsp.transpose(parts[4], 2.0)) for i in range(128 * 2)]) ]

        layers += [ ''.join([dsp.env(dsp.transpose(parts[0], 2.0) * 2, 'phasor') for i in range(32 * 3)]) ]
        layers += [ ''.join([dsp.env(dsp.transpose(parts[0], 1.5) * 2, 'phasor') for i in range(32 * 3)]) ]
        layers += [ ''.join([dsp.env(dsp.transpose(parts[0], 4.0) * 2, 'phasor') for i in range(64 * 2)]) ]
        layers += [ ''.join([dsp.env(dsp.transpose(parts[0], 4.5) * 2, 'line') for i in range(64 * 2)]) ]
        layers += [ ''.join([dsp.env(dsp.transpose(parts[0], 3.0), 'phasor') for i in range(64 * 2)]) ]

        plongs = dsp.split(parts[4], dsp.flen(parts[4]) / 16)
        plongs = [dsp.env(p, 'sine', True) for p in plongs]
        plongs = [dsp.randchoose(plongs) for i in range(64 * len(plongs) * 2)]

        layers += [ ''.join(plongs) ]

        layers = [dsp.pan(l, dsp.rand()) for l in layers]

        out += dsp.amp(dsp.mix(layers, False), 3.0)

        return out

    def beats(self, out=''):
        parts = dsp.split(self.drums.data, dsp.flen(self.drums.data) / 8)

        out += ''.join([parts[2] for i in range(8)])
        out += dsp.amp(''.join([parts[6] for i in range(8)]), 2.0)

        return dsp.amp(out, 2.0)

    def mess(self, out=''):
        parts = dsp.split(self.master.data, dsp.flen(self.master.data) / 16)

        etypes = ['line', 'phasor', 'sine', 'cos', 'tri', 'saw', 'flat']
        beats = dsp.split(parts[1], dsp.beat / 3)
        beats = [dsp.panenv(dsp.randchoose(beats), dsp.randchoose(etypes), 'line') for b in beats]
        out += ''.join([''.join(dsp.randshuffle(beats)) for i in range(8)])

        beats = dsp.split(parts[14], dsp.beat)
        beats = [dsp.env(dsp.randchoose(beats), 'phasor') for b in beats]
        out += ''.join([''.join(dsp.randshuffle(beats)) for i in range(8)])

        beats = dsp.split(parts[3], dsp.beat / 3)
        beats = [dsp.env(dsp.randchoose(beats), 'line') for b in beats]
        out += ''.join([''.join(dsp.randshuffle(beats)) for i in range(8)])

        beats = dsp.split(parts[14], dsp.beat / 3)
        beats = [dsp.panenv(dsp.randchoose(beats), dsp.randchoose(etypes), 'phasor') for b in beats]
        out += ''.join([''.join(dsp.randshuffle(beats)) for i in range(8)])

        return out

      
if __name__ == '__main__':
    main()
