import time
import logging

import browser 
import repo_mysql 
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

class spider:
	def __init__(self,repo_name='test',user='yyttrr3242342@163.com',passwd=None):
		self.dl=browser.browser(user,passwd)
		self.repo=repo_mysql.repo_mysql(repo_name)

		self.log=runlog('spider')

		self.searched=dict()
		self.searched['friendList']=self.repo.getSearched('friendList')
		self.searched['status']=self.repo.getSearched('status')
		self.searched['profile']={}#self.repo.getSearched('profile')

	def login(self):
		return self.dl.login()

	def getStatus_friend(self,orig_id='410941086'):
		pageStyle='status'
		if orig_id not in self.searched[pageStyle]:
			self.seq_process(orig_id,pageStyle)
		friends=self.repo.getFriendList(orig_id)
		toSearch=friends-self.searched[pageStyle]
		self.log.info('{} of {},toSearch/total:{}/{}'.format('friends\' status',orig_id,len(toSearch),len(friends)))
		self.seq_process(toSearch,'status')

	def getNet2(self,orig_id='410941086'):
		pageStyle='friendList'
		if orig_id not in self.searched[pageStyle]:
			self.seq_process(orig_id,pageStyle)
		friends=self.repo.getFriendList(orig_id)
		toSearch=friends-self.searched[pageStyle]
		self.log.info('get net2 of {},toSearch/total:{}/{}'.format(orig_id,len(toSearch),len(friends)))
		self.seq_process(toSearch,'friendList')

	def seq_process(self,toSearch,pageStyle):
		"""download and save record of `toSearch` in target pageStyle"""
		if isinstance(toSearch,str):
			toSearch={toSearch}
		for i,rid in zip(range(1,len(toSearch)+1),toSearch):
			meth_download=getattr(browser.browser,pageStyle)
			record,run_info=meth_download(self.dl,rid)
			if record is None:
				self.log.error('{},{},error info:{}'.format(rid,pageStyle,run_info))
			else:
				meth_save=getattr(repo_mysql.repo_mysql,'save_{}'.format(pageStyle))
				n=meth_save(self.repo,record,rid,run_info)
				log_text='{}/{},saved/download:{}/{},{} of {}, time={}'.format(i,len(toSearch),n,len(record),pageStyle,rid,run_info)
				if n<len(record):
					self.log.error(log_text)
				else:
					self.log.info(log_text)
					self.searched[pageStyle].add(rid)


def getProfile_friend(rid='410941086'):
	print('{} start to get profile of {}\'s friends'.format(time.strftime('%H:%M:%S',time.localtime()),rid))
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
				print('{}/{}, saved/browser:{}/{} profile of {}'.format(i,len(toSearch),n,len(pf),rid))
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
			info='{}/{},saved/browser:{}/{},status of {}, time={}'.format(i,len(toSearch),len(stat),n,rid,timecost)
			if n<len(stat):
				log.error(info)
			else:
				log.info(info)
	#TODO:deal with timeout list
	#print('timeout list: {}'.format(timeout_list()))

