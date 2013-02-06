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

	def test_status(self):
		stat={'4373362607': {'timestamp': '2012-12-13 06:50', 'cur_content': '我的移动硬盘貌似坏了。。。(img囧-窘迫img)(img囧-窘迫img)(img囧-窘迫img)怎么办啊。。。我靠它活了活了这么久了。。。 ', 'orig_owner': None, 'orig_content': None, 'cur_owner': '284874220'}, '4377919606': {'timestamp': '2012-12-14 13:47', 'cur_content': '貌似一切都弄完了。。。(img谄笑img)(img谄笑img)(img谄笑img) ', 'orig_owner': None, 'orig_content': None, 'cur_owner': '284874220'}, '4233651348': {'timestamp': '2012-10-31 23:41', 'cur_content': '认真的男生最有魅力了。。。(img流口水img)(img流口水img)(img流口水img) ', 'orig_owner': None, 'orig_content': None, 'cur_owner': '284874220'}, '4018789023': {'timestamp': '2012-08-30 21:23', 'cur_content': '冷死了。。。 ', 'orig_owner': None, 'orig_content': None, 'cur_owner': '284874220'}, '4376534598': {'timestamp': '2012-12-14 00:09', 'cur_content': '生日快乐。。。哈哈，又老了一岁(img尴尬img)(img尴尬img)(img尴尬img) ', 'orig_owner': None, 'orig_content': None, 'cur_owner': '284874220'}, '4209110693': {'timestamp': '2012-10-24 14:45', 'cur_content': '每次看完韩剧就有流不完的眼泪。。。(img哭img)(img哭img)(img哭img) ', 'orig_owner': None, 'orig_content': None, 'cur_owner': '284874220'}, '4247563975': {'timestamp': '2012-11-05 05:16', 'cur_content': '好诡异的梦。。。竟然、、、 ', 'orig_owner': None, 'orig_content': None, 'cur_owner': '284874220'}, '4265658479': {'timestamp': '2012-11-10 14:01', 'cur_content': '你们这群愚蠢的地球人。。。哈哈哈哈 ', 'orig_owner': None, 'orig_content': None, 'cur_owner': '284874220'}, '3728866382': {'timestamp': '2012-06-19 20:35', 'cur_content': '海的女儿。。。转自href(p699170020p) ', 'orig_owner': '699170020', 'orig_content': "【12星座的童话代表】白羊——画眉嘴国王的妻子；金牛——魔镜； 双子——小裁缝；巨蟹——豌豆公主；狮子——穿新装的皇帝； 处女——温顺的老太太；天秤——格蕾特尔；天蝎——匹诺曹；射手——海的女儿；摩羯——灰姑娘；水瓶——苯汉汉斯；双鱼——白雪公主。（了解更多自己星座的奥秘，关于上升星座和月亮星", 'cur_owner': '284874220'}}
		print(self.db.status(stat))

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
	suite.addTest(TestRenrenDb('test_status'))
	#suite.addTest(TestRenrenDb('testTableManage'))
	#suite.addTest(TestRenrenDb('test_getFriendList'))
	#suite.addTest(TestRenrenDb('testGetRenrenId'))
	#suite.addTest(TestRenrenDb('testGetSearched'))
	runner=unittest.TextTestRunner()
	runner.run(suite)
