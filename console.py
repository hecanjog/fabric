import cmd
import subprocess
import dsp
import os

class Fabric(cmd.Cmd):

    prompt = 'fabric: '
    intro = 'A just-in-realtime console.'

    def play(self, cmd):
        shhh = open(os.devnull, 'w')
        p = subprocess.Popen(['python'] + cmd, shell=False, stdout=shhh)
        shhh.close()
        print 'playing', cmd[0] 

    def do_p(self, cmd):
        self.play(['haiku.py'] + cmd.split(' '))
        print cmd

    def do_EOF(self, line):
        return True

    def postloop(self):
        """ cleanup """
        pass

    
if __name__ == '__main__':
    console = Fabric()
    console.cmdloop()
