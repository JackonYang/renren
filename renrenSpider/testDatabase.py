import unittest
from database import *

class TestRenrenDb(unittest.TestCase):

	def setUp(self):
		self.db=database()
		#self.db.dropTempTable()
		#self.db.createTempTable()#not exists

	def tearDown(self):
		#self.db.dropTempTable()
		self.db.close()
		self.db=None

	def test_friendList(self):
		names=[{'266754031':'王瑛','27331442':'Ethan.王哲','240303471':'刘洋English','239439171':'','222439171':'eeee','324134134':'～！@#￥%……&*（）'},dict(),None,set()]
		for name in names:
			print(name)
			print(self.db.friendList('11111',name))
	def test_profile(self):
		pfs={'profile_detail':{'大学': '西北大学- 2011年- 物理学系<br>', '高中': '阳光中学- 2008年', '初中': '西安交通大学阳光中学- 2005年'},'profile_detail':{'小学': '烟台市芝罘区新海阳小学- 1995年', '家乡': '山东 烟台市', '生日': ' 1989 年3 月 11 日双鱼座', '高中': '烟台二中- 2004年', '初中': '烟台二中- 2000年', '个性域名': 'wangzhongzhe.renren.com', '性别': '男', '大学': '西北大学- 2007年- 物理学系<br>山东大学- 2012年- 电气工程学院<br>'},'profile_mini':{'gender': '女生', 'location': '烟台市'}}
		rids=['111','222','333']
		for rid,pf in zip(rids,pfs.items()):
			print('{},{}'.format(rid,self.db.profile(rid,pf[1],pf[0])))

	def testGetSearched(self):
		name={'266754031':'王瑛','27331442':'Ethan.王哲','240303471':'刘洋English','239439171':'','222439171':'eeee','324134134':'～！@#￥%……&*（）'}
		renrenId='11111'
		maindb_rid1='101'
		self.db.friendList(renrenId,name)

		self.assertEquals(self.db.getSearched('friendList'),{renrenId,maindb_rid1})
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
	def test_getFriendList(self):
		self.save=database('renren_orig')
		print(len(self.save.getFriendList('410941086')))
		print(len(self.save.getFriendList('233330059')))

	def testTableManage(self):
		self.db.dropTempTable()
		self.db.createTempTable()#not exists
		self.db.createTempTable()#exists
		self.db.dropTempTable()#exists
		self.db.dropTempTable()#not exists

		self.db.createMainTable()#not exists

if __name__=='__main__':
	suite=unittest.TestSuite()
	#suite.addTest(TestRenrenDb('test_friendList'))
	suite.addTest(TestRenrenDb('test_profile'))
	#suite.addTest(TestRenrenDb('testTableManage'))
	#suite.addTest(TestRenrenDb('test_getFriendList'))
	#suite.addTest(TestRenrenDb('testGetRenrenId'))
	#suite.addTest(TestRenrenDb('testGetSearched'))
	runner=unittest.TextTestRunner()
	runner.run(suite)
