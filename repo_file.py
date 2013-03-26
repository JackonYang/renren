# -*- coding: utf-8-*-
import pickle
import time

save_period=240  # second
class repo_file:
	def __init__(self, name_pre='test'):
		self.data_repo={}
		self.name_pre=name_pre
		self.last_saved=time.time()

	def __del__(self):
		self.save('__del__')

	def load(self, pageStyle):
		filename='{}_{}.p'.format(self.name_pre, pageStyle)
		try:
			with open(filename, 'rb') as f:
				self.data_repo[pageStyle]=pickle.load(f)
		except IOError:
				self.data_repo[pageStyle]=dict()

	def save(self,orig=None):
		for pageStyle, record in self.data_repo.items():
			filename='{}_{}.p'.format(self.name_pre, pageStyle)
			with open(filename, 'wb') as f:
				pickle.dump(record, f)
				self.last_saved = time.time()
				#print('save in {}, called by {}'.format(filename,orig))

	def save_friendList(self, record, rid, run_info=None):
		"""save record and return rows affected.save nothing if empty.
		return None if input error"""
		return self._save_process('friendList', record, rid, run_info)

	def save_status(self, record, rid, run_info=None):
		"""save record and return rows affected.save nothing if empty.
		return None if input error"""
		return self._save_process('status', record, rid, run_info)

	def save_profile(self, record, rid, run_info=None):
		"""save profile and return rows affected.return None if input error"""
		return self._save_process('profile', record, rid, run_info)

	def _save_process(self, pageStyle, record, rid, run_info):
		if not isinstance(record,dict):
			return None
		if pageStyle not in self.data_repo:
			self.load(pageStyle)
		self.data_repo[pageStyle][rid]=record
		# save to file every n second
		global save_period
		if time.time() - self.last_saved > save_period:
			self.save('auto')
		return len(record)

	def getSearched(self, pageStyle):
		if pageStyle not in self.data_repo:
			self.load(pageStyle)
		return set(self.data_repo[pageStyle].keys())

	def getFriendList(self, renrenId):
		pageStyle='friendList'
		if pageStyle not in self.data_repo:
			self.load(pageStyle)
		return set(self.data_repo[pageStyle].get(renrenId,{}))
