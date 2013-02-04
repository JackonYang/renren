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
#pf_detail_searched=save.getSearched('profile_detail')

def getNet2(rid='410941086'):
	log.debug('{} start to search net2 of {}'.format(time.strftime('%H:%M:%S',time.localtime()),rid))
	timeout_list=set()
	fl,timecost=dl.friendList(rid)
	save.friendList(rid,fl)
	toSearch=set(fl.keys())-fl_searched
	log.debug('{} renrenId={},toSearch/total:{}/{}'.format(time.strftime('%H:%M:%S',time.localtime()),rid,len(toSearch),len(fl)))
	for i,item in zip(range(len(toSearch)),toSearch):
		friends,timecost=dl.friendList(item)
		if friends is None:
			timeout_list.add(rid)
		else:
			n=save.friendList(item,friends)
			if n>0:
				log.info('{}/{} download/saved:{}/{},net2 of {},{},{},{}'.format(i+1,len(toSearch),len(friends),n,rid,item,fl[item],timecost))
			else:
				log.warn('{}/{} friendList privacy.download:{},{},{}'.format(i+1,len(toSearch),len(friends),item,fl[item]))
	log.debug('{} net2 of {} done'.format(time.strftime('%H:%M:%S',time.localtime()),rid))
	#TODO:deal with timeout list
	#print('timeout list: {}'.format(timeout_list()))

def getProfile_friend(rid='410941086'):
	print('{} start to search profile of {}'.format(time.strftime('%H:%M:%S',time.localtime()),rid))
	timeout_list=set()
	friends=save.getFriendList(item)
	#save.profile_detail(rid,fl)
	toSearch=set(friends)-pf_detail_searched
	print('{} renrenId={},toSearch/total:{}/{}'.format(time.strftime('%H:%M:%S',time.localtime()),rid,len(toSearch),len(friends)))
	for i,item in zip(range(len(toSearch)),toSearch):
		pf_detail=dl.profile_detail(rid)
		if friends is None:
			timeout_list.add(rid)
		else:
			n=save.friendList(item,friends)
			if n>0:
				log.info('{}/{} download/saved:{}/{},net2 of {},{},{},{}'.format(i+1,len(toSearch),len(friends),n,rid,item,fl[item],timecost))
			else:
				log.warn('{}/{} friendList privacy.download:{},{},{}'.format(i+1,len(toSearch),len(friends),item,fl[item]))
	log.debug('{} net2 of {} done'.format(time.strftime('%H:%M:%S',time.localtime()),rid))
	#TODO:deal with timeout list
	#print('timeout list: {}'.format(timeout_list()))

if __name__ == '__main__':
	#rid=input('renrenId= ')
	#getNet2('233330059')
	getNet2('224227137')
	#getNet2('410941086')
	#getNet2('285060168')
	save.close()
