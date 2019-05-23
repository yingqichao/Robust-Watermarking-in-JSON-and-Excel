import sys
import time


class Logger(object):
    def __init__(self, filename=time.strftime('./log/%Y%m%d%H%M', time.localtime(time.time()))+'.log', stream=sys.stdout):
        self.terminal = stream
        if filename != None:
            self.log = open(filename, 'a')
        else:
            self.log = None
        self.str = ''

    def write(self, message):
        self.str = self.str + message + '\n'
        self.terminal.write(message+'\n')
        if self.log != None:
            self.log.write(message+'\n')


    def flush(self):
        pass
