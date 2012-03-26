import dsp
import wes
import sounds

vs = dsp.split(sounds.vg.data, 200)

for i in range(1000):
    size = dsp.randint(3, 30), dsp.randint(40, 1000)
    lpitch = dsp.rand(0.00001, 3)
    hpitch = lpitch + dsp.rand(0.01, 3)
    pitches = dsp.breakpoint([wes.rword('worhjkhskjsd', lpitch, hpitch) for s in range(size[0])], size[1])
    offset = dsp.randint(0, len(vs) - size[1] - 1)

    vv = ''
    for p in range(size[1]):
        vv += dsp.transpose(vs[offset + p], pitches[p % len(pitches)-1])

    vv = dsp.benv(vv, [0] + [dsp.rand(0.2, 1) for i in range(size[0])])
    dsp.play(vv)

    dsp.delay(dsp.rand(0, dsp.rand(0.001, 10)))

