import unittest
import repo_file
import os

def clear(filenames):
	for filename in filenames:
		os.remove(filename)
		#print('rm {}'.format(filename))

class new_file(repo_file.repo_file):
	def file_to_clear(self):
		filenames=[]
		for pageStyle in self.data_repo:
			filenames.append('{}_{}.p'.format(self.name_pre,pageStyle))
		return filenames

class test_repo_mysql(unittest.TestCase):

	def setUp(self):
		self.repo=new_file()

	def tearDown(self):
		f=self.repo.file_to_clear()
		self.repo=None  # save again
		clear(f)

	def test_save_friendList(self):
		names=[({'266754031':'王瑛','27331442':'Ethan.王哲','240303471':'刘洋English','239439171':'','222439171':'eeee','324134134':'～！@#￥%……&*（）'},6),(dict(),0),(None,None),({'3','4'},None)]
		for name,expt in names:
			self.assertEquals(self.repo.save_friendList(name,'11111'),expt)
			self.repo.save()

	def test_save_status(self):
		stats=[({'3352227193': {'cur_name': '張曉旭', 'timestamp': '2012-04-08 12:32', 'cur_content': '(img酷img)', 'orig_content': "you\'re ok. Let's do something\\", 'orig_name': '闷骚青年', 'orig_owner': '600992999', 'renrenId1': '410941086'}, 
			'2956159738': {'cur_name': '張曉旭', 'timestamp': '2012-01-08 00:58', 'cur_content': "'蛋舍k歌中'", 'orig_content': None, 'orig_name': None, 'orig_owner': None, 'renrenId1': '410941086'}, 
			'4268947468': {'cur_name': '張曉旭', 'timestamp': '2012-11-11 10:59', 'cur_content': '光棍节快乐 各位~', 'orig_content': None, 'orig_name': None, 'orig_owner': None, 'renrenId1': '410941086'}, 
			'3369389870': {'cur_name': '張曉旭', 'timestamp': '2012-04-11 17:59', 'cur_content': '哈哈转自(427674621,韩丹虹):转自(390845915,马焱意):恩 恩 @赵文轩帅哥，你火了耶～～转自(385023791,任慧)', 'orig_content': '南区的说 、物理系体操队 中间的男生好帅。 话说、中间的是赵文轩吧。。。好吧 应该的。(img流口水img)', 'orig_name': '任慧', 'orig_owner': '385023791', 'renrenId1': '410941086'}},4),(dict(),0),(None,None),({'3','4'},None)]
		for stat,expt in stats:
			self.assertEquals(self.repo.save_status(stat,'11111'),expt)
			self.repo.save()

	def test_getSearched(self):
		stat1={'81': {'cur_name': 'name1', 'timestamp': '2012-01-08 00:58', 'cur_content': "'蛋舍k歌中'", 'orig_content': None, 'orig_name': None, 'orig_owner': None, 'renrenId1': '71'}}
		stat2={'82': {'cur_name': 'name1', 'timestamp': '2012-02-08 00:58', 'cur_content': "'蛋舍k歌中'", 'orig_content': None, 'orig_name': None, 'orig_owner': None, 'renrenId1': '72'}}
		self.repo.save_friendList({'91':'name1'},'11','success')
		self.repo.save_friendList({'92':'name2'},'12','timecost_info')
		self.repo.save_friendList({},'13','timecost_info')
		self.repo.save_friendList(None,'14','timeout')
		expt_friendList={'11','12','13'}
		self.repo.save_status(stat1,'21','success')
		self.repo.save_status(stat2,'22','timecost_info')
		self.repo.save_status({},'23','timecost_info')
		self.repo.save_status(None,'24','timeout')
		expt_status={'21','22','23'}

		self.assertEquals(self.repo.getSearched('friendList'),expt_friendList)
		self.assertEquals(self.repo.getSearched('status'),expt_status)

	def test_getFriendList(self):
		name={'266754031':'王瑛','27331442':'Ethan.王哲','240303471':'刘洋English','239439171':'','222439171':'eeee','324134134':'～！@#￥%……&*（）'}
		name2={'231':'王瑛','2442':'Ethan.王哲','241':'刘洋English','2171':'','439171':'eeee','324134134':'～！@#￥%……&*（）'}
		renrenId='100032076'
		renrenId2='103076'
		self.repo.save_friendList(name,renrenId)
		self.repo.save_friendList(name2,renrenId2)
		self.repo.save()

		self.assertEquals(self.repo.getFriendList(renrenId),set(name.keys()))
		self.assertEquals(self.repo.getFriendList(renrenId2),set(name2.keys()))

if __name__=='__main__':
	suite=unittest.TestSuite()

	suite.addTest(test_repo_mysql('test_save_status'))
	suite.addTest(test_repo_mysql('test_save_friendList'))
	suite.addTest(test_repo_mysql('test_getSearched'))
	suite.addTest(test_repo_mysql('test_getFriendList'))

	runner=unittest.TextTestRunner()
	runner.run(suite)
