"""log in 4 files"""

import logging
import os

logLvl = logging.DEBUG


def getLogger(formatter, path, name=''):
    log = logging.getLogger(name)
    log.setLevel(logLvl)
    lvls = ['Debug', 'info', 'warn', 'error']

    if not os.path.exists(path):
        os.mkdir(path)

    for lvl in lvls:
        logfile = os.path.join(path, '{}.log'.format(lvl.lower()))
        hdlr = logging.FileHandler(logfile)
        hdlr.setLevel(getattr(logging, lvl.upper()))
        hdlr.setFormatter(formatter)
        log.addHandler(hdlr)
    return log


def debugLog():
    path = os.path.join(os.path.dirname(__file__), 'log/debug')
    formatter = logging.Formatter('%(asctime)s|%(levelname)s|%(message)s|%(filename)s-%(lineno)s')
    return getLogger(formatter, path, 'debug')


class runLog:
    def __init__(self):
        path = os.path.join(os.path.dirname(__file__), 'log/run')
        formatter = logging.Formatter('%(asctime)s|%(message)s')
        self.log = getLogger(formatter, path, 'debug.run')

    def out(self, message, timecost):
        log.info('%s. Time cost: %s' % (message.strip(' .'), timecost))


if __name__ == '__main__':
    log = debugLog()
    log.error('test log')
    log.info('info log')

    log2 = runLog()
    log2.out('write run log', 2)
