#!/usr/bin/env python

import os

__all__ = ["traceBegin", "traceEnd", "Trace", "trace"]

__TRACE_MARKER = '/sys/kernel/debug/tracing/trace_marker'

if os.access(__TRACE_MARKER, os.W_OK):
    __TRACE_FILE = open(__TRACE_MARKER, 'w')
    __PID = str(os.getpid())
    def traceBegin(name):
        buf = '|'.join(('B', __PID, name))
        __TRACE_FILE.write(buf)
        try:
            __TRACE_FILE.flush()
        except IOError:
            pass
    
    def traceEnd():
        __TRACE_FILE.write('E')
        try:
            __TRACE_FILE.flush()
        except IOError:
            pass
else:
    traceBegin = lambda name: None 
    traceEnd = lambda: None

class Trace:
    def __init__(self, name):
        traceBegin(name)
    def __del__(self):
        traceEnd()

class trace:
    def __init__(self, name = ''):
        self.name = name

    def __call__(self, func):
        if not self.name:
            self.name = func.__name__
        def wrapper(*args):
            t = Trace(self.name)
            return func(*args)
        return wrapper

def main():
    import time

    @trace()
    def sleep(duration):
        time.sleep(duration)

    class Sleep:
        @trace()
        def __init__(self):
            pass

        @trace()
        def sleep(self, duration):
            time.sleep(duration)

    # test manual trace
    traceBegin('Manual_Sleep')
    time.sleep(1)
    traceEnd()

    time.sleep(1)

    # test trace decorator
    sleep(1)

    s = Sleep()
    s.sleep(1)

if __name__ == '__main__':
    main()

# vim: ts=4 st=4 sts=4 expandtab syntax=python
