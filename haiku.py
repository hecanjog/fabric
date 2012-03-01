import dsp

dsp.timer('start')

out = ''
thirty = 44100 * 2 * 2 * 30;

for i in range(thirty):
    d = i % (thirty / 100) + 1
    s = i % d
    out += chr(s % 256)

print dsp.write(out, 'haiku-12-03-01-thirtyc', False)
dsp.timer('stop')
