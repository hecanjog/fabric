import dsp
import re

scale = [1.0, 1.125, 1.25, 1.333, 1.5, 1.667, 1.875, 2.0]
freqs = [196.0, 293.7, 440.0, 659.3]
ratios = [1.0, 1.5, 2.0, 3.0]
wtypes = ['line', 'phasor', 'sine', 'tri', 'impulse', 'phasor']
poem = ''
crword = []

def read(poem):
    """ Ignore whitespeace and read words and lines """
    poem = poem.split("\n")
    poem = [line.strip() for line in poem]
    poem = [line for line in poem if line is not '']

    for i, line in enumerate(poem):
        line = line.split(' ')
        line = [word.strip() for word in line]
        line = [re.sub('[\W_]+', '', word) for word in line]
        poem[i] = [word for word in line if line is not '']
    
    return poem 

def readline(linestart=0):
    global poem

    if poem == '':
        load()

    linelog = open('linepos.txt', 'r+')
    cpos = int(linelog.readline())

    if cpos > len(poem) - 1:
        cpos = 0

    line = poem[cpos]

    cpos += 1

    linelog.seek(0)
    linelog.write(str(cpos))
    linelog.close()
    
    return line

def load(f='poems.txt'):
    global poem 
    global poemlen
    f = open(f, 'r')

    poem = read(f.read())

    return poem

def rchoose(word, l):
    return l[int(rword(word) * (len(l)-1))]

def rword(word, low=0.0, high=1.0, recurse=True):
    global crword

    if crword == []:
        crword = list(word)

    letter = translate(crword[0]) * (high - low) + low
    crword.pop(0)

    return letter

def numchars(line, count=0):
    for word in line:
        count += len(word)

    return count

def translate(letter):
    """ Translate standard ASCII chars into 0 - 1 float values """

    l = ord(letter)

    # space, tab, new line, \r
    if l == 32 or l == 9 or l == 10 or l == 13: 
        return 0
    
    # symbols
    if l >= 33 and l <= 47:
        return (l - 32) / 32.0
            
    if l >= 58 and l <= 64:
        return (l - 57 + 15) / 32.0
    
    if l >= 91 and l <= 96:
        return (l - 90 + 15 + 7) / 32.0

    if l >= 123 and l <= 126:
        return (l - 122 + 15 + 7 + 6) / 32.0

    # numerals
    if l >= 48 and l <= 57:
        return (l - 47) / 10.0

    # uppercase alpha
    if l >= 65 and l <= 90:
        if l == 90:
            return 1.0

        return (l - 64) / 25.99

    # lowercase alpha
    if l >= 97 and l <= 122:
        return (l - 96) / 26.0
    
    return 0
