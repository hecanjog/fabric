#!/usr/bin/env python2
# -*- coding: UTF-8 -*-

""" Ding dong :: www.hecanjog.com
"""

import wave
import audioop
import math
import random
import struct
import string
import time
import hashlib

from datetime import datetime

audio_params = (2, 2, 44100, 0, "NONE", "not_compressed") 
snddir = '' 
dsp_grain = 64
env_min = 2 
cycle_count = 0
thetime = 0
seedint = 0
seedstep = 0
seedhash = ''

def lget(list, index, default=True):
    try:
        return list[index]
    except IndexError:
        if default == True:
            return list[-1]
        else:
            return list[0]

def interleave(list_one, list_two):
    # find the length of the longest list
    if len(list_one) > len(list_two):
        big_list = len(list_one)
    elif len(list_two) > len(list_one):
        big_list = len(list_two)
    else:
        if randint(0, 1) == 0:
            big_list = len(list_one)
        else:
            big_list = len(list_two)

    combined_lists = []

    # loop over it and insert alternating items
    for index in range(big_list):
        if index <= len(list_one) - 1:
            combined_lists.append(list_one[index])
        if index <= len(list_two) - 1:
            combined_lists.append(list_two[index])

    return combined_lists

def packet_shuffle(list, packet_size):
    """
        Takes a list, splits it into sub-lists of size N
        and shuffles those lists, then collapes them into 
        original list
    """
    if packet_size >= 3 and packet_size <= len(list):
        lists = list_split(list, packet_size)
        shuffled_lists = []
        for sublist in lists:
            shuffled_lists.append(randshuffle(sublist))

        big_list = []
        for shuffled_list in shuffled_lists:
            big_list.extend(shuffled_list)
        return big_list

def string_split(audio_string, length):
    packets = len(audio_string) / length
    return [audio_string[length*i:(length*i)+length] for i in range(packets)]

def list_split(list, packet_size):
    trigs = []
    for i in range(len(list)):
        if i % int(packet_size) == 0:
            trigs.append(i)

    newlist = []

    for trig_index, trig in enumerate(trigs):
        if trig_index < len(trigs) - 1:
            packets = []
            for packet_bit in range(packet_size):
                packets.append(list[packet_bit + trig])

            newlist.append(packets)

    return newlist

def ratio(numerator, denominator):
    return float(numerator) / float(denominator)

def timer(cmd='start'):
    global thetime
    if cmd == 'start':
        thetime = time.time()
        print 'Started render at timestamp', thetime
        return thetime 
    elif cmd == 'stop':
        thetime = time.time() - thetime
        themin = int(thetime) / 60
        thesec = thetime - (themin * 60)
        print 'Render time:', themin, 'min', thesec, 'sec'
        return thetime

def transpose(audio_string, amount):
    amount = 1.0 / amount

    audio_string = audioop.ratecv(audio_string, 2, 2, 44100, int(44100 * amount), None)
    
    return audio_string[0]

def byte_string(number):
    return struct.pack("<h", number)

def tone(length=44100, freq=440, wavetype='sine2pi', amp=1.0, blocksize=0):
    cyclelen = htf(freq * 0.99)
    numcycles = length / cyclelen

    if blocksize > 0:
        numblocks = numcycles / blocksize
        if numcycles % blocksize > 0:
            numblocks += 1

        cycles = ''.join([blocksize * cycle(freq * rand(0.99, 1.0), wavetype, amp) for i in range(numblocks)])
    else:
        cycles = numcycles * cycle(freq * rand(0.99, 1.0), wavetype, amp)

    if(flen(cycles) < length):
        print 'too short!', fts(length - flen(cycles))
    print 'generated a tone', fts(flen(cycles)), 'seconds long'
    print

    return cycles 

def cycle(freq, wavetype='sine2pi', amp=1.0):
    wavecycle = wavetable(wavetype, htf(freq))
    return ''.join([byte_string(cap(amp * s * 32767, 32767, -32768)) * audio_params[0] for s in wavecycle])

def scale(low_target, high_target, low, high, pos):
    pos = float(pos - low) / float(high - low) 
    return pos * float(high_target - low_target) + low_target
    
def cap(num, max, min=0):
    if num < min:
        num = min
    elif num > max:
        num = max
    return num

def seed(theseed=False):
    global seedint
    global seedhash

    if theseed == False:
        theseed = cycle(440)

    h = hashlib.sha1(theseed)
    seedhash = h.digest()

    seedint = int(''.join([str(ord(c)) for c in list(seedhash)]))
    return seedint

def stepseed():
    global seedint
    global seedstep

    h = hashlib.sha1(str(seedint))
    seedint = int(''.join([str(ord(c)) for c in list(h.digest())]))

    seedstep = seedstep + 1

    return seedint
    

def randint(lowbound=0, highbound=1):
    global seedint

    if seedint > 0:
        return int(rand() * (highbound - lowbound) + lowbound)
    else:
        return random.randint(lowbound, highbound)


def rand(lowbound=0, highbound=1):
    global seedint
    if seedint > 0:
        return ((stepseed() / 100.0**20) % 1.0) * (highbound - lowbound) + lowbound
    else:
        return random.random() * (highbound - lowbound) + lowbound

def randchoose(items):
    return items[randint(0, len(items)-1)]

def randshuffle(input):
    items = input[:]
    shuffled = []
    for i in range(len(items)):
        if len(items) > 0:
            item = randchoose(items)
            shuffled.append(item)
            items.remove(item)

    return shuffled 


def breakpoint(values, size=512, range_out=(0,1)):
    if len(values) > 1:
        steps = size / (len(values) - 1)
        steps_remainder = size % (len(values) - 1)
    else:
        print 'breakpoint fail: one or fewer values'

    groups = []

    for i, v in enumerate(values):
        if i == len(values) - 2:
            steps += steps_remainder
        
        if i < len(values) - 1:
            if steps - 1 > 0:
                groups.extend([(c / float(steps - 1)) * (values[i+1] - v) + v for c in range(steps)]) 
            else:
                print size, steps, i, v, len(values), 'breakpoint fail'

    return groups

def wavetable(wtype="sine", size=512):
    wtable = []
    wave_types = ["sine", "cos", "line", "saw", "impulse", "phasor", "sine2pi", "cos2pi"]

    if wtype == "random":
        wtype = wave_types[randint(0, len(wave_types) - 1)]
    if wtype == "sine":
        wtable = [math.sin(i * math.pi) for i in frange(size)]
    elif wtype == "sine2pi":
        wtable = [math.sin(i * math.pi * 2) for i in frange(size)]
    elif wtype == "cos2pi":
        wtable = [math.cos(i * math.pi * 2) for i in frange(size)]
    elif wtype == "cos":
        wtable = [math.cos(i * math.pi) for i in frange(size)]
    elif wtype == "saw":
        wtable = [(i - 1.0) * 2.0 for i in frange(size)]
    elif wtype == "line":
        wtable = [i for i in frange(size)]
    elif wtype == "phasor":
        wtable = wavetable("line", size)
        list.reverse(wtable)
    elif wtype == "impulse":
        wtable = [float(randint(-1, 1)) for i in range(size / randint(2, 12))]
        wtable.extend([0.0 for i in range(size - len(wtable))])
    elif wtype == "vary":
        if size < 10:
            print 'vary size small:', size
            wtable = wavetable("random", size)
        else:
            wtable = breakpoint([rand() for i in range(4)], size) 

    wtable[0] = 0.0
    wtable[-1] = 0.0
    
    return wtable

def frange(steps):
    if steps < env_min:
        steps = env_min
    return [ i / float(steps - 1) for i in range(steps)]

def env(audio_string, wavetable_type="sine"):
    packets = split(audio_string, dsp_grain)
    wtable = wavetable(wavetable_type, len(packets))
    packets = [audioop.mul(packet, audio_params[1], wtable[i]) for i, packet in enumerate(packets)]

    return ''.join(packets) 

def alias(audio_string, passthru = 0, envelope = 'random', split_size = 0):
    if passthru > 0:
        return audio_string

    if envelope == 'flat':
        envelope = False

    if split_size == 0:
        split_size = dsp_grain / randint(1, dsp_grain)

    packets = split(audio_string, split_size)
    packets = [p*2 for i, p in enumerate(packets) if i % 2]

    out = ''.join(packets)

    if envelope:
        out = env(out, envelope)

    return out 

def log(message, mode="a"):
    logfile = open("tmplog.txt", mode)
    logfile.write(str(message) + "\n")
    return logfile.close()

def fill(string, length):
    if flen(string) < length:
        repeats = length / flen(string) + 1
        string = string * repeats

    return cut(string, 0, length)

def mix(layers, leftalign=True, boost=2.0):
    """ mixes N stereo audio strings """
    attenuation = 1.0 / len(layers)
    attenuation *= boost 
    layers.sort(key = len)
    output_length = flen(layers[-1])

    out = pad('', output_length, 0) 

    for layer in layers:
        padding = output_length - flen(layer) 

        if leftalign:
            layer = pad(layer, 0, padding)
        else:
            layer = pad(layer, padding, 0)

        layer = audioop.mul(layer, audio_params[1], attenuation)

        if len(layer) != ftc(output_length) or len(out) != ftc(output_length):
            dif = int(math.fabs(len(layer) - len(out)))
            print 'unequal', dif
            if len(out) < len(layer):
                layer = layer[:len(layer) - dif]
            else:
                out = out[:len(out) - dif]

        out = audioop.add(out, layer, audio_params[1])

    return out 

def flen(string):
    # string length in frames
    return len(string) / (audio_params[1] + audio_params[0])

def pad(string, start, end):
    # start and end given in samples, as usual 
    # eg lengths of silence to pad at start and end

    zero = struct.pack('<h', 0)
    zero = zero[0:1] * audio_params[1] * audio_params[0] # will we ever have a width > 2? donno.

    return "%s%s%s" % ((start * zero), string, (end * zero))


def amp(string, scale):
    return audioop.mul(string, audio_params[1], scale)

def prob(item_dictionary):
    weighted_list = []
    for item, weight in item_dictionary.iteritems():
        for i in range(weight):
            weighted_list.append(item)

    return randchoose(weighted_list)

def stf(s):
    ms = s * 1000.0
    return mstf(ms)

def mstf(ms):
    frames_in_ms = audio_params[2] / 1000.0
    frames = ms * frames_in_ms

    return int(frames)

def ftms(frames):
    ms = frames / float(audio_params[2]) 
    return ms * 1000

def fts(frames):
    s = frames / float(audio_params[2])
    return s

def ftc(frames):
    frames = int(frames)
    frames *= audio_params[1] # byte width
    frames *= audio_params[0] # num chans

    return frames

def htf(hz):
    """ hz to frames """
    if hz > 0:
        frames = audio_params[2] / float(hz)
    else:
        frames = 1 # 0hz is okay...

    return int(frames)

def timestamp_filename():
    current_time = str(datetime.time(datetime.now()))
    current_time = string.replace(current_time, ":", ".")
    current_date = str(datetime.date(datetime.now()))

    return current_date + "_" + current_time + "_"

def write(audio_string, filename, timestamp = True, dirname="renders"):
    if timestamp == True:
        filename = dirname + '/' + filename + '-' + timestamp_filename() + '.wav' 
    else:
        filename = dirname + '/' + filename + '.wav'
    wavfile = wave.open(filename, "w")
    wavfile.setparams(audio_params)
    wavfile.writeframes(audio_string)
    wavfile.close()
    return filename

def read(filename):
    filename = snddir + filename
    print 'loading', filename

    file = wave.open(filename, "r")
    file_frames = file.readframes(file.getnframes())

    snd = Sound()

    # check for mono files
    if file.getnchannels() == 1:
        file_frames = audioop.tostereo(file_frames, file.getsampwidth(), 0.5, 0.5)
        snd.params = file.getparams()
        snd.params = (2, snd.params[1], snd.params[2], snd.params[3], snd.params[4], snd.params[5])
    else:
        snd.params = file.getparams()

    snd.data = file_frames

    return snd

def pan(audio_string, amps = (1, 1), passthru = False):
    if passthru:
        return audio_string

    if audio_params[0] == 1:
        audio_string = audioop.tostereo(audio_string, audio_params[1], amps[0], amps[1])
    elif audio_params[0] == 2:
        audio_string = audioop.tomono(audio_string, audio_params[1], 0.5, 0.5)
        audio_string = audioop.tostereo(audio_string, audio_params[1], amps[0], amps[1])

    return audio_string

def spread(packets, width = (1, 1), prob = 0.5):
    packets = [pan(p, (width[0] * rand(), width[1] * rand()), probability(prob)) for p in packets]

    return packets

def probability(prob):
    # returns weighted random boolean 
    return rand() > prob

def insert_into(haystack, needle, position):
    # split string at position index
    hay = cut(haystack, 0, position)
    stack = cut(haystack, position, flen(haystack) - position)
    return "%s%s%s" % (hay, needle, stack)

def replace_into(haystack, needle, position):
    hayend = position * audio_params[1] * audio_params[0]
    stackstart = hayend - (flen(needle) * audio_params[1] * audio_params[0])
    return "%s%s%s" % (haystack[:hayend], needle, haystack[stackstart:])

def cut(string, start, length):
    # start and length are both given in frames (aka samples)za

    if start + length > flen(string):
        print 'No cut for you!'

    length = int(length) * audio_params[1] * audio_params[0]
    start = int(start) * audio_params[1] * audio_params[0]

    return string[start : start + length]

def check_string(string):
    # Check to see if the input string divides evenly by the byte width
    if len(string) % audio_params[1] * audio_params[0] > 0:
        print 'dsp.split(): your string is probably fucked up. check your math.'

def split(string, size):
    # size is given in frames (aka samples)

    # Multiply the number of frames we want by the current byte width
    frames = int(size) * audio_params[1] * audio_params[0]

    check_string(string)

    return [string[frames * count : (frames * count) + frames] for count in range(len(string) / frames)]

def vsplit(input, minsize, maxsize):
    # min/max size is in frames...
    output = []
    pos = 0

    for chunk in range(flen(input) / minsize):
        chunksize = randint(minsize, maxsize)
        if pos + chunksize < flen(input) - chunksize:
            output.append(cut(input, pos, chunksize))
            pos += chunksize

    return output

def walk(snd_flen, range=(0,1), position=(0,10)):
    start = snd_flen * float(range[0])
    end = snd_flen * float(range[1])

    pos = float(position[0]) / float(position[1])

    pos *= end - start
    pos += start

    #print '    walk!', range, position, pos

    return int(pos)

def bpm2ms(bpm):
    return 60000.0 / float(bpm)

def bpm2frames(bpm):
    return int((bpm2ms(bpm) / 1000.0) * audio_params[2]) 

def argr(args, k, v):
    args[k] = v
    return args

def pantamp(pan_pos):
    # Translate the pan position into a tuple size two of left amp and right amp
    if pan_pos > 0.5:
        pan_pos -= 0.5
        pan_pos *= 2.0
        pan_pos = 1.0 - pan_pos
        pan_pos = (pan_pos, 1.0)
    elif pan_pos < 0.5:
        pan_pos *= 2.0
        pan_pos = (1.0, pan_pos)
    else:
        pan_pos = (1.0, 1.0)

    return pan_pos

def rangetowidth(low, high):
    width = high - low
    width += low
    return width

def train(sound, pulses=10, pos=(0.0, 1.0, [0.0, 1.0, 0.0], 'sine'), freq=(0.0, 1.0, [0.0, 1.0, 0.0], 'sine'), amp=(0.0, 1.0, [1.0], 'sine'), pan=(0.0, 1.0, [1.0], 'sine')):
    pass

def pulsar(sound, freq=(1.0, 1.01, 'random'), amp=(0.0, 1.0, 'random'), pan_pos=0.5):
    slices = split(sound, dsp_grain)

    # Set pulsaret parameters
    out_params = {
            'amp': (amp[0], amp[1], wavetable(amp[2], len(slices))),
            'freq': (freq[0], freq[1], wavetable(freq[2], len(slices))),
            'pan_amp': pantamp(pan_pos),
    }

    # Process each dsp_grain length packet with subpulse() - packets returned can be of variable size
    slices = [pulsaret(slice, out_params, i) for i, slice in enumerate(slices)]

    # Join packets into pulse and return the audio string
    return ''.join(slices)
   
def pulsaret(slice, params, index):
    amp = ((params['amp'][1] - params['amp'][0]) * params['amp'][2][index]) + params['amp'][0]

    lslice = audioop.tomono(slice, audio_params[1], 1, 0)
    lslice = audioop.tostereo(lslice, audio_params[1], params['pan_amp'][0], 0)

    rslice = audioop.tomono(slice, audio_params[1], 0, 1)
    rslice = audioop.tostereo(rslice, audio_params[1], 0, params['pan_amp'][1])

    slice = audioop.add(lslice, rslice, audio_params[1])
    slice = audioop.mul(slice, audio_params[1], amp)

    freq_width = params['freq'][2][index] * (params['freq'][1] - params['freq'][0]) + params['freq'][0]
    target_rate = int(audio_params[2] * (1.0 / float(freq_width)))

    if target_rate == audio_params[2]:
        return slice
    else:
        if target_rate < dsp_grain or target_rate > 2147483647:
            print target_rate
            
        slice = audioop.ratecv(slice, audio_params[0], audio_params[1], audio_params[2], cap(target_rate, 2147483647, dsp_grain), None)
        return slice[0]

def fnoise(sound, coverage):
    target_frames = int(flen(sound) * coverage)

    for i in range(target_frames):
        p = randint(0, flen(sound) - 1)
        f = cut(sound, p, 1)
        sound = replace_into(sound, f, randint(0, flen(sound) - 1))

    return sound

class Sound:
    def __init__(self):
        data = ''
        params = ''
