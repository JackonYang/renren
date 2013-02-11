import unittest
import repo_mysql 

class new_mysql(repo_mysql.repo_mysql):
	def clearTable(self):
		for table in self.table.values():
			self.cur.execute('drop table if exists {}'.format(table))
		self.conn.commit()

class test_repo_mysql(unittest.TestCase):

	def setUp(self):
		self.db=new_mysql()

	def tearDown(self):
		self.db.clearTable() 
		self.db=None

	def test_save_friendList(self):
		names=[({'266754031':'王瑛','27331442':'Ethan.王哲','240303471':'刘洋English','239439171':'','222439171':'eeee','324134134':'～！@#￥%……&*（）'},6),(dict(),0),(None,None),({'3','4'},None)]
		for name,expt in names:
			self.assertEquals(self.db.save_friendList(name,'11111'),expt)

	def test_save_status(self):
		stats=[({'3352227193': {'cur_name': '張曉旭', 'timestamp': '2012-04-08 12:32', 'cur_content': '(img酷img)', 'orig_content': "Let's do something\\", 'orig_name': '闷骚青年', 'orig_owner': '600992999', 'renrenId1': '410941086'}, 
			'2956159738': {'cur_name': '張曉旭', 'timestamp': '2012-01-08 00:58', 'cur_content': "'蛋舍k歌中'", 'orig_content': None, 'orig_name': None, 'orig_owner': None, 'renrenId1': '410941086'}, 
			'4268947468': {'cur_name': '張曉旭', 'timestamp': '2012-11-11 10:59', 'cur_content': '光棍节快乐 各位~', 'orig_content': None, 'orig_name': None, 'orig_owner': None, 'renrenId1': '410941086'}, 
			'3369389870': {'cur_name': '張曉旭', 'timestamp': '2012-04-11 17:59', 'cur_content': '哈哈转自(427674621,韩丹虹):转自(390845915,马焱意):恩 恩 @赵文轩帅哥，你火了耶～～转自(385023791,任慧)', 'orig_content': '南区的说 、物理系体操队 中间的男生好帅。 话说、中间的是赵文轩吧。。。好吧 应该的。(img流口水img)', 'orig_name': '任慧', 'orig_owner': '385023791', 'renrenId1': '410941086'}},4),(dict(),0),(None,None),({'3','4'},None)]
		for stat,expt in stats:
			self.assertEquals(self.db.save_status(stat,'11111'),expt)

	def test_save_history(self):
		log_info=('1111','profile','success','123')
		stat={'2956159738': {'cur_name': '張曉旭', 'timestamp': '2012-01-08 00:58', 'cur_content': "'蛋舍k歌中'", 'orig_content': None, 'orig_name': None, 'orig_owner': None, 'renrenId1': '410941086'}}
		self.assertEquals(self.db.save_history(*log_info),1)
		self.assertEquals(self.db.save_friendList({'1':'name1'},'11','success'),1)
		self.assertEquals(self.db.save_status(stat,'22','timeout'),1)

	def test_save_profile(self):
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

	def test_tableManage(self):
		self.db.clearTable()
		tableTag=['history','friendList','status','name']
		for tag in tableTag:
			self.db._init_table(tag)
			self.db._init_table(tag)
		self.db.clearTable()
		for tag in tableTag:
			self.db._init_table(tag)

if __name__=='__main__':
	suite=unittest.TestSuite()
	#suite.addTest(test_repo_mysql('test_profile'))
	#suite.addTest(test_repo_mysql('test_getFriendList'))
	#suite.addTest(test_repo_mysql('testGetRenrenId'))
	#suite.addTest(test_repo_mysql('testGetSearched'))

	#checked
	suite.addTest(test_repo_mysql('test_save_status'))
	suite.addTest(test_repo_mysql('test_save_friendList'))
	suite.addTest(test_repo_mysql('test_tableManage'))
	suite.addTest(test_repo_mysql('test_save_history'))

	runner=unittest.TextTestRunner()
	runner.run(suite)
