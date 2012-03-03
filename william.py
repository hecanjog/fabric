import dsp

def main(out=''):
    s = """recently
    I awoke and briefly remembered
    everything I meant to detail
    about the specifics of dreamspace

    except
    the tonal suggestion of your quiet bones
    concentically ripple-sliding in fractalized
    friction like windchime moans
    predetermining escapes to overlapping
    internally fictional colour landscapes
    
    wc tank 
    """

    dsp.seed(s)
    dsp.timer('start')

    dsp.snddir = 'sounds/william/'
    score = Score()

    timings = score.timings(dsp.stf(dsp.randint(60, 300)))
    timings.extend(score.timings(dsp.stf(dsp.randint(60,300))))
    timings.extend(score.timings(dsp.stf(dsp.randint(60,300))))

    out += dsp.env(score.sines(dsp.stf(dsp.randint(2, 8))), 'vary')

    for t in timings:
        out += score.section(t)

    out = dsp.write(out, 'william', True)

    out += dsp.env(score.sines(dsp.stf(dsp.randint(2, 8))), 'vary')

    # Show render time
    dsp.timer('stop')
    print dsp.seedstep, 'hashes calculated'

class Score:
    """ structure, score """

    tonic = 440.0

    scale = [
        1.0,
        2.222,
        2.5,
        3.0,
        4.0,
      ]

    def __init__(self):
        self.pitches = []
        for s in self.scale:
            self.pitches.append((s / self.scale[-1]) * self.tonic)

    def timings(self, total_length):
        # Must have at least four points, the more the better... 
        if len(self.scale) < 4:
            return [0] 

        # Select between 2 and N-2 timing points
        numselections = dsp.randint(2, len(self.scale)-2)
        # Sort input so low and high bounds are in 0 and -1 index positions
        self.scale.sort()

        # Pull inner points from the scale, the low and high bounds are 
        # always included as a minumum
        selectionset = self.scale[1:-1]
        selections = []

        # Select a variable set of points from the set
        for n in range(numselections):
            selection = selectionset[dsp.randint(0, len(selectionset)-1)]
            selections.append(selection)
            selectionset.remove(selection)

        # Insert low and high bounds once again and sort everything
        selections.append(self.scale[0])
        selections.append(self.scale[-1])
        selections.sort()

        # Calculate the distance between selected points as ratios and 
        # scale the input length against it to determine section lengths

        # Account for the low and high bounds 
        numselections = len(selections)

        section_lengths = []

        for i, s in enumerate(selections[1:]):
            s = s - selections[i] # A little tricky: this index refers to the prev point
            s = s / (selections[-1] - selections[0])
            section_lengths.append(int(s * total_length))

        return dsp.randshuffle(section_lengths)

    def section(self, length, out=''):
        layers = []

        if dsp.randint(0, 6) > 1:
            out += dsp.env(self.sines(dsp.mstf(dsp.randint(200, 4000))), 'vary')

        layers.append(dsp.amp(self.sines(length), 0.7))
        layers.append(dsp.amp(self.sines(length), 0.7))
        layers.append(dsp.env(dsp.amp(self.sines(length), 1.1), 'vary'))
        layers.append(dsp.env(dsp.amp(self.sines(length), 1.1), 'vary'))

        layers.append(dsp.amp(self.pulses(length), 2.0))
        layers.append(dsp.env(dsp.amp(self.pulses(length), 2.0), 'vary'))

        layers.append(dsp.amp(self.phases(length), 2.0))
        layers.append(dsp.amp(self.phases(length), 2.5))
        layers.append(dsp.amp(self.phases(length), 2.5))
        layers.append(dsp.amp(self.phases(length), 2.5))
        layers.append(dsp.amp(self.phases(length), 2.0))

        layers.append(dsp.env(self.trains(length), 'vary'))
        layers.append(dsp.env(self.trains(length), 'vary'))
        layers.append(dsp.env(self.trains(length), 'vary'))

        out += dsp.mix(layers, 2.3) 

        if dsp.randint(0, 3) > 1:
            out += dsp.mix([self.pulses(dsp.mstf(dsp.randint(200, 4000))) for i in range(dsp.randint(3, 8))])
        
        return out

    def trains(self, length, out=''):
        print 'trains!', dsp.fts(length)
        wtypes = ['sine2pi', 'vary', 'saw', 'cos2pi', 'impulse', 'vary']
        trainlens = self.timings(length)
        for t in trainlens:
            wtype = wtypes[dsp.randint(0, len(wtypes)-1)]
            trains = dsp.split(self.train(t, wtype), trainlens[dsp.randint(0, len(trainlens)-1)] / dsp.randint(2, 16))
            trains = [dsp.env(dsp.pulsar(train), 'vary') for train in trains]
            trains = ''.join(dsp.randshuffle(trains))

            if dsp.randint(0, 4) < 4:
                trains = dsp.alias(trains, 0, 'vary', dsp.randint(8, 12))

            out += trains

        return out

    def phases(self, length, out=''):
        print 'phases!', dsp.fts(length)
        wtypes = ['vary', 'sine2pi', 'saw', 'vary', 'cos2pi', 'impulse', 'vary']
        
        pulselens = self.timings(length / dsp.randint(10, 120))
        pulselen = pulselens[dsp.randint(0, len(pulselens)-1)]

        layers = []
        for l in range(dsp.randint(2, 4)):
            wtype = wtypes[dsp.randint(0, len(wtypes)-1)]
            layers.append(dsp.pulsar(self.train(length, wtype)))

        phases = []
        for i in range(dsp.randint(2, 4)): 
            il = dsp.randint(0, len(layers)-1)
            phase = dsp.split(layers[il], pulselen) 
            phase = [dsp.env(p, 'phasor') for p in phase]
            ppad = [int(iw) for iw in dsp.wavetable('random', len(phase), 0.0, dsp.rand(44.0, 44100.0))]
            phase = [dsp.pad(p, 0, ppad[ip]) for ip,p in enumerate(phase)]
            phase = ''.join(dsp.randshuffle(phase))
            phase = dsp.fill(phase, length)
            phases.append(dsp.env(phase, 'vary'))

        out += dsp.mix(phases)

        return out


    def pulses(self, length, out=''):
        print 'pulses!', dsp.fts(length)
        wtypes = ['sine2pi', 'saw', 'cos2pi', 'impulse']
        layers = []
        wtype = wtypes[dsp.randint(0, len(wtypes)-1)]
        trains = [self.train(length, wtype) for i in range(dsp.randint(2, 4))]
        for t in trains:
            trainlens = []
            traindiv = dsp.randint(32, 64)
            for i in range(traindiv):
                trainlens.extend(self.timings(length / traindiv))

            pulses = []
            for l in trainlens:
                start = dsp.randint(0, dsp.flen(t) - l)
                pulse = dsp.cut(t, start, l)
                pulse = dsp.env(pulse, 'vary')
                pulse = dsp.cut(pulse, 0, dsp.flen(pulse) / 2)
                pulse = dsp.pad(pulse, 0, dsp.flen(pulse))
                freq = (0.999, 1.001, 'vary')
                amp = (0.5, 0.9, 'vary')
                pulse = dsp.pulsar(pulse, freq, amp, dsp.rand())
                pulses.append(pulse)
            pulses = ''.join(pulses)
            pulses = dsp.fill(pulses, length)
            layers.append(pulses)

        out = dsp.mix(layers)

        return out

    def train(self, length, wtype='impulse', out=''):
        print '    train!', dsp.fts(length), wtype
        layers = [ dsp.pulsar(dsp.tone( length
                            ,self.pitches[dsp.randint(0, len(self.pitches)-1)] * dsp.randchoose([1,2,4,8,16,32])
                            ,wtype
                            ,dsp.rand(0.01, 0.2) ))
                    for i in range(dsp.randint(3,6)) ]

        out += dsp.mix(layers)

        return out

    def sines(self, length, out=''):
        print 'sines!', dsp.fts(length)
        layers = [ dsp.pulsar(dsp.tone( length 
                            ,self.pitches[dsp.randint(0,len(self.pitches)-1)] * dsp.randchoose([1,2,4,8,16,32])
                            ,'sine2pi' 
                            ,dsp.rand(0.01, 0.2) )) 
                   for i in range(dsp.randint(3,6)) ]

        out += dsp.mix(layers)
        
        return out

      
if __name__ == '__main__':
    main()
