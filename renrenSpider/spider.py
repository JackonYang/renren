import time
import logging

import download
import database
import parse


def runlog(tt='run'):
		logfile='run.log'
		logger=logging.getLogger(tt)
		hdlr=logging.FileHandler(logfile)
		formatter=logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
		hdlr.setFormatter(formatter)
		logger.addHandler(hdlr)
		logger.setLevel(20)#20 info, 40 error
		return logger

pf_sleep=3
user='jiekunyang@gmail.com'
dl=download.download(user)
save=database.database('renren_orig')
log=runlog()


fl_searched=save.getSearched('friendList')
pf_searched=save.getSearched('profile')
status_searched=save.getSearched('status')

def getNet2(orig_id='410941086'):
	print('start to search net2 of {}'.format(orig_id))
	timeout_list=set()
	fl,timecost=dl.friendList(orig_id)
	save.friendList(orig_id,fl)
	toSearch=set(fl.keys())-fl_searched
	print('{} get net2 of {},toSearch/total:{}/{}'.format(time.strftime('%H:%M:%S',time.localtime()),orig_id,len(toSearch),len(fl)))
	for i,rid in zip(range(1,len(toSearch)+1),toSearch):
		friends,timecost=dl.friendList(rid)
		if friends is None:
			print('error.friendList None.renrenid={}'.format(rid))
			timeout_list.add(rid)
		else:
			n=save.friendList(rid,friends)
			info='{}/{},saved/download:{}/{},friendList of {}, time={}'.format(i,len(toSearch),len(friends),n,rid,timecost)
			if n<len(friends):
				log.error(info)
			else:
				log.info(info)
	#TODO:deal with timeout list
	#print('timeout list: {}'.format(timeout_list()))

def getProfile_friend(rid='410941086'):
	print('{} start to search friend profile of {}'.format(time.strftime('%H:%M:%S',time.localtime()),rid))
	timeout_list=set()
	friends=save.getFriendList(rid)
	toSearch=set(friends)-pf_detail_searched
	print('{} renrenId={},toSearch/total:{}/{}'.format(time.strftime('%H:%M:%S',time.localtime()),rid,len(toSearch),len(friends)))
	for i,item in zip(range(1,len(toSearch)+1),toSearch):
		pf=dl.profile_detail(item)
		if pf is None:
			timeout_list.add(item)
		else:
			n=save.profile_detail(item,pf)
			if n>0:
				print('{}/{} {}'.format(i,len(toSearch),item))
				time.sleep(pf_sleep)
			else:
				print('{}/{} profile no items.{}'.format(i,len(toSearch),item))
	#log.debug('{} net2 of {} done'.format(time.strftime('%H:%M:%S',time.localtime()),rid))
	#TODO:deal with timeout list
	#print('timeout list: {}'.format(timeout_list()))

def getProfile():
	timeout_list=set()
	toSearch=fl_searched-pf_searched
	print('{} get profiles toSearch/total:{}/{}'.format(time.strftime('%H:%M:%S',time.localtime()),len(toSearch),len(fl_searched)))
	for i,rid in zip(range(1,len(toSearch)+1),toSearch):
		pfStyle,pf=dl.profile(rid)
		if pf is None:
			print('error.profile None.renrenid={},pfStyle={}'.format(rid,pfStyle))
			timeout_list.add(rid)
		elif pf == {}:
			save.profile_empty(rid,pfStyle)
		else:
			if pfStyle == 'detail':
				n=save.profile(rid,pf,'profile_detail')
			else:
				n=save.profile(rid,pf,'profile_mini')
			if n == 0:
				print('{}/{}, saved/download:{}/{} profile of {}'.format(i,len(toSearch),n,len(pf),rid))
		if pfStyle == 'detail':
			time.sleep(pf_sleep)
		if i%50 == 0:
			log.info('{}/{} profiles done'.format(i,len(toSearch)))
	#TODO:deal with timeout list
	#print('timeout list: {}'.format(timeout_list()))

def getStatus():
	timeout_list=set()
	toSearch=fl_searched-status_searched
	print('{} get status toSearch/total:{}/{}'.format(time.strftime('%H:%M:%S',time.localtime()),len(toSearch),len(fl_searched)))
	for i,rid in zip(range(1,len(toSearch)+1),toSearch):
		stat,timecost=dl.status(rid)
		if stat is None:
			print('error.status None,renrenId={}'.format(rid))
			timeout_list.add(rid)
		else:
			n=save.status(stat)
			info='{}/{},saved/download:{}/{},status of {}, time={}'.format(i,len(toSearch),len(stat),n,rid,timecost)
			if n<len(stat):
				log.error(info)
			else:
				log.info(info)
	#TODO:deal with timeout list
	#print('timeout list: {}'.format(timeout_list()))

