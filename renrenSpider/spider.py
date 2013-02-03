import time
import logging

import download
import database


def runlog(tt='run'):
		logfile='run.log'
		logger=logging.getLogger(tt)
		hdlr=logging.FileHandler(logfile)
		formatter=logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
		hdlr.setFormatter(formatter)
		logger.addHandler(hdlr)
		logger.setLevel(20)#20 info, 40 error
		return logger

user='jiekunyang@gmail.com'
dl=download.download(user)
save=database.database('renren_orig')
log=runlog()


fl_searched=save.getSearched('friendList')

def getNet2(rid='410941086'):
	log.debug('{} start to search net2 of {}'.format(time.strftime('%H:%M:%S',time.localtime()),rid))
	timeout_list=set()
	fl,timecost=dl.friendList(rid)
	save.friendList(rid,fl)
	toSearch=set(fl.keys())-fl_searched
	log.info('{} renrenId={},toSearch/total:{}/{}'.format(time.strftime('%H:%M:%S',time.localtime()),rid,len(toSearch),len(fl)))
	for i,item in zip(range(len(toSearch)),toSearch):
		friends,timecost=dl.friendList(item)
		if friends is None:
			timeout_list.add(rid)
		else:
			n=save.friendList(item,friends)
			log.info('{}/{} {},{},{} friends,{} saved,{}'.format(i,len(toSearch),item,fl[item],len(friends),n,timecost))
	log.info('{} net2 of {} done'.format(time.strftime('%H:%M:%S',time.localtime()),rid))
	#TODO:deal with timeout list
	#print('timeout list: {}'.format(timeout_list()))


if __name__ == '__main__':
	#rid=input('renrenId= ')
	getNet2('233330059')
	save.close()
