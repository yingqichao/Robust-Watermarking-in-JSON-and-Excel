import sys
import time


class Logger(object):
    def __init__(self, filename=time.strftime('./log/%Y%m%d%H%M', time.localtime(time.time()))+'.log', stream=sys.stdout):
        self.terminal = stream
        self.log = open(filename, 'a')

    def write(self, message):
        self.terminal.write(message+'\n')
        self.log.write(message+'\n')

    def flush(self):
        pass
