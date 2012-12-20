import os
import inspect
import sys

class PrintTracer(object):
    stdout = None
    enabled = False
    flushed = True
    traceNumber = 0

    @staticmethod
    def enable():
        if not PrintTracer.enabled:
            PrintTracer.enabled = True
            PrintTracer.stdout = sys.stdout
            sys.stdout = PrintTracer

    @staticmethod
    def disable():
        if PrintTracer.enabled:
            PrintTracer.enabled = False
            sys.stdout = PrintTracer.stdout

    @staticmethod
    def write(s):
        curframe = inspect.currentframe()
        calframe = inspect.getouterframes(curframe, 2)
        if s == '\n' and not PrintTracer.flushed:
            PrintTracer.flushed = True
            path = calframe[1][1]
            name = os.path.basename(path)
            if name == '__init__.py':
                name = os.path.basename(os.path.dirname(path))+'/'+name
            s = ' (%s: %s, traceno: %s)\n'%(calframe[1][2], name, PrintTracer.traceNumber)
            PrintTracer.traceNumber += 1
        else:
            PrintTracer.flushed = False
        PrintTracer.stdout.write(s)

    @staticmethod
    def flush():
        pass

def enable():
    return PrintTracer.enable()

def disable():
    return PrintTracer.disable()