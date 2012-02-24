import cmd
import subprocess
import os

class Fabric(cmd.Cmd):
    prompt = 'fabric: '
    intro = 'A just-in-realtime console.'

    def play(self, cmd):
        orcs = os.listdir('orc/')
        for orc in orcs:
            if cmd[0] == orc[0:2]:
                cmd[0] = 'orc/' + orc
                shhh = open(os.devnull, 'w')
                p = subprocess.Popen(['python'] + cmd, shell=False, stdout=shhh)
                shhh.close()
                print 'playing', cmd
                return True

        print 'not found'

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
