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
	def test_profile_detail(self):
		pfs={'11111':{'edu_college': '西北大学-2007年-物理学系<br>山东大学-2012年-电气工程学院<br>', 'edu_primary': '烟台市芝罘区新海阳小学-1995年', 'edu_junior': '烟台二中-2000年', 'gender': '男', 'edu_senior': '烟台二中-2004年', 'birth': '1989年3月11日双鱼座', 'hometown': '山东烟台市', 'domain2': 'wangzhongzhe.renren.com'},'2222':{'qq': '309097050', 'edu_college': '西北大学-2013年-其它院系<br>', 'edu_primary': '', 'edu_junior': '西安四中', 'personal_website': '', 'msn': '', 'gender': '男', 'company': '', 'phone': '15191895258', 'edu_senior': '西安交通大学附中-1999年', 'birth': '1998年2月13日<!--水瓶座-->水瓶座', 'hometown': '内蒙古呼伦贝尔市', 'edu_tech': '西安市二轻局职工中等专业学校'},'33333':{'edu_college': '西北大学-2011年-物理学系<br>', 'edu_junior': '西安交通大学阳光中学-2005年', 'edu_senior': '阳光中学-2008年'},'5555':{},'6666':None}
		for rid,pf in pfs.items():
			print('{},{}'.format(rid,self.db.profile_detail(rid,pf)))

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
	suite.addTest(TestRenrenDb('test_profile_detail'))
	#suite.addTest(TestRenrenDb('testTableManage'))
	#suite.addTest(TestRenrenDb('test_getFriendList'))
	#suite.addTest(TestRenrenDb('testGetRenrenId'))
	#suite.addTest(TestRenrenDb('testGetSearched'))
	runner=unittest.TextTestRunner()
	runner.run(suite)
