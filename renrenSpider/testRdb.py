import unittest
from db import *

class TestRenrenDb(unittest.TestCase):

	def setUp(self):
		self.db=rDb()
		#self.db.dropTempTable()
		#self.db.createTempTable()#not exists

	def tearDown(self):
		#self.db.dropTempTable()
		self.db.close()
		self.db=None

	def testInsertFriendList(self):
		name={'266754031':'王瑛','27331442':'Ethan.王哲','240303471':'刘洋English','239439171':'','222439171':'eeee','324134134':'～！@#￥%……&*（）'}
		self.db.insertFriendList('11111',name)
	def testGetSearched(self):
		name={'266754031':'王瑛','27331442':'Ethan.王哲','240303471':'刘洋English','239439171':'','222439171':'eeee','324134134':'～！@#￥%……&*（）'}
		renrenId='11111'
		origId='101'
		exptName=set(name.keys())
		exptName.add(origId)
		self.db.insertFriendList(renrenId,name)

		self.assertEquals(self.db.getSearched('name'),exptName)
		self.assertEquals(self.db.getSearched('relation'),{renrenId,origId})
	def testGetRenrenId(self):
		name={'266754031':'王瑛','27331442':'Ethan.王哲','240303471':'刘洋English','239439171':'','222439171':'eeee','324134134':'～！@#￥%……&*（）'}
		name2={'231':'王瑛','2442':'Ethan.王哲','241':'刘洋English','2171':'','439171':'eeee','324134134':'～！@#￥%……&*（）'}
		a='324134134'#last key of name2
		renrenId='100032076'
		renrenId2='103076'
		self.db.insertFriendList(renrenId,name)
		self.db.insertFriendList(renrenId2,name2)
		self.assertEquals(self.db.getRenrenId(2,renrenId),set(name.keys()))
		self.assertEquals(self.db.getRenrenId(2,renrenId2),set(name2.keys()))
		self.assertEquals(self.db.getRenrenId(1,renrenId2),set())
		self.assertEquals(self.db.getRenrenId(1,'101'),{'101'})
		#self.assertEquals(self.db.getRenrenId(1,a),{renrenId2})

	def testTableManage(self):
		self.db.dropTempTable()
		self.db.createTempTable()#not exists
		self.db.createTempTable()#exists
		self.db.dropTempTable()#exists
		self.db.dropTempTable()#not exists

		self.db.createMainTable()#not exists

if __name__=='__main__':
	suite=unittest.TestSuite()
	#suite.addTest(TestRenrenDb('testInsertFriendList'))
	#suite.addTest(TestRenrenDb('testTableManage'))
	#suite.addTest(TestRenrenDb('testGetRenrenId'))
	suite.addTest(TestRenrenDb('testGetSearched'))
	runner=unittest.TextTestRunner()
	runner.run(suite)
