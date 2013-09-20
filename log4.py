"""log in 4 files"""

import logging
import os


def getLogger(root='', path='log'):
    log = logging.getLogger(root)
    log.setLevel(logging.DEBUG)
    lvls = ['debug', 'info', 'warn', 'error']
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    if not os.path.exists(path):
        os.mkdir(path)

    for lvl in lvls:
        logfile = os.path.join(path, '{}.log'.format(lvl))
        hdlr = logging.FileHandler(logfile)
        hdlr.setLevel(getattr(logging, lvl.upper()))
        hdlr.setFormatter(formatter)
        log.addHandler(hdlr)
    return log

if __name__ == '__main__':
    log = getLogger()
    log.error('test log')
    log.info('info log')
