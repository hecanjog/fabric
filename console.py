import cmd
import subprocess
import os
import dsp
import wes
import sounds

dsp.quiet = True

class Fabric(cmd.Cmd):
    prompt = 'fabric: '
    intro = 'A just-in-realtime console.'

    poempos = 0

    def play(self, cmd):
        orcs = os.listdir('orc/')
        for orc in orcs:
            if cmd[0] == orc[0:2]:
                cmd.pop(0)
                orc = 'orc.' + orc.split('.')[0]
                p = __import__(orc, globals(), locals(), ['play'])
                process = dsp.poly(p.play, [sounds] + cmd + ['l:' + str(self.poempos)])

                print 'playing', orc, cmd
                return True

        print 'not found'

    def do_swell(self, cmd):
        orcswell = __import__('orc.swell', globals(), locals(), ['play'])
        dsp.poly(orcswell.play, [sounds] + cmd.split(' '))

    def default(self, cmd):
        self.play(cmd.split(' '))

    def do_EOF(self, line):
        return True

    def postloop(self):
        """ cleanup """
        pass
    
if __name__ == '__main__':
    console = Fabric()
    console.cmdloop()
