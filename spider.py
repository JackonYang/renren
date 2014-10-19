# -*- coding: utf-8-*-
import time
import os
import logging
import downloader
import repo_mysql

def debug_log(rel_path='log/spider'):
    path = os.path.join(os.path.dirname(__file__), rel_path)
    formatter = logging.Formatter('%(asctime)s|%(levelname)s|%(message)s|%(filename)s-%(lineno)s')

    log = logging.getLogger('renre.spider')
    log.setLevel(logging.INFO)
    lvls = ['debug', 'info', 'warn', 'error']

    if not os.path.exists(path):
        os.makedirs(path)

    for lvl in lvls:
        logfile = os.path.join(path, '{}.log'.format(lvl.lower()))
        hdlr = logging.FileHandler(logfile)
        hdlr.setLevel(getattr(logging, lvl.upper()))
        hdlr.setFormatter(formatter)
        log.addHandler(hdlr)
    return log


pf_sleep=2
class spider:
    def __init__(self, cookie):
        self.dl = downloader.renren(cookie)
        self.repo = repo_mysql.repo_mysql()
        self.login_id = self.dl.renrenId()
        self.fl_searched = self.repo.get_fl_searched()
        self.log = debug_log()

    def getNet1(self, orig_id):
        if not isinstance(orig_id, str):
            print('ERROR! str required. orig_id = %s' % orig_id)
            return None
        if orig_id not in self.fl_searched:
            print('{} download net1 of {}'.format(time.strftime('%H:%M:%S', time.localtime()), orig_id))
            record = self.dl.friendList(orig_id)
            if record is None:
                self.log.error('{}, fail to download friend list.'.format(rid))
            else:
                self.repo.save_fl(self.login_id, orig_id, record)
        return self.repo.get_fl(orig_id)

    def getNet2(self, orig_id):
        friends = self.getNet1(orig_id)
        toSearch = friends - self.fl_searched
        print('{} get net2 of {}, toSearch/total: {}/{}'.format(time.strftime('%H:%M:%S',time.localtime()), orig_id, len(toSearch), len(friends)))
        for i, rid in zip(range(1, len(toSearch)+1), toSearch):
            record = self.dl.friendList(rid)
            if record is None:
                self.log.error('{}, fail to download friend list.'.format(rid))
            else:
                saved = self.repo.save_fl(self.login_id, rid, record)
                log_text = '{}/{}, newName/friends: {}/{}, friendlist of {}'.format(i, len(toSearch), saved, len(record), rid)
                if saved > 0:
                    self.log.info(log_text)
                    self.fl_searched.add(rid)
                else:
                    self.log.error(log_text)

    def getStatus_friend(self,orig_id='410941086'):
        pageStyle='status'
        if pageStyle not in self.searched:
            self.searched[pageStyle]=self.repo.getSearched(pageStyle)
        friends=self.getNet1(orig_id)
        toSearch=(friends|{orig_id})-self.searched[pageStyle]
        print('{} {} of {},toSearch/total:{}/{}'.format(time.strftime('%H:%M:%S',time.localtime()),'friends\' status',orig_id,len(toSearch),len(friends)+1))
        self.seq_process(toSearch,pageStyle)

    def getProfile_friend(self,orig_id='410941086'):
        pageStyle='profile'
        if pageStyle not in self.searched:
            self.searched[pageStyle]=self.repo.getSearched(pageStyle)
        friends=self.getNet1(orig_id)
        toSearch=(friends|{orig_id})-self.searched[pageStyle]
        print('{} {} of {},toSearch/total:{}/{}'.format(time.strftime('%H:%M:%S',time.localtime()),'friends\' profile',orig_id,len(toSearch),len(friends)+1))
        self.seq_process(toSearch,pageStyle)


if __name__ == '__main__':
    test_cookie = raw_input('Input cookie(document.cookie): ')

    runner = spider(test_cookie)

    # start by login id
    print runner.getNet2(runner.login_id)
