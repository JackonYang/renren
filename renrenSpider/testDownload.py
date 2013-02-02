import unittest
from download import download

class Test_download(unittest.TestCase):

	def setUp(self):
		#user='yyttrr3242342@163.com'
		user='jiekunyang@gmail.com'
		self.dl=download(user)
	def tearDown(self):
		pass

	def test_profile_detail(self):
		renrenIds={'233330059','230760442','223981104','410941086','285060168'}
							#myself,timeline ok/unavailable,old style ok/unavailable
		for rid in renrenIds:
			info=self.dl.profile_detail(rid)
			print('{},{}'.format(rid,info))

	def test_friendList(self):
		renrenIds={'233330059','410941086','267654044','285060168','240303471'}
							#myself,3+pages/2pages/1page/unavailable
		for rid in renrenIds:
			fl,timecost=self.dl.friendList(rid)
			print('{},{},{}'.format(rid,len(fl),timecost))
		#flist={'232639310':35,'242543024':152,'285060168':5}
		#for item in flist.items():
			#self.assertEqual(len(self.browser.friendList(item[0])),item[1])

	def test_homepage(self):
		renrenIds={'233330059','410941086','267654044','285060168','240303471'}
		for rid in renrenIds:
			info=self.dl.homepage(rid)
			print('{},{}'.format(rid,info))

	def test_login(self):
		users=['yyttrr3242342@163.com','jiekunyang@gmail.com','zhangxiaoxu_521@yahoo.com.cn','none@adaf.com']
		rids=['498934189','233330059','410941086',None]
		for user,rid in zip(users,rids):
			dl=download(user)

if __name__=='__main__':
	suite=unittest.TestSuite()
	#suite.addTest(Test_download('test_friendList'))
	#suite.addTest(Test_download('test_profile_detail'))
	suite.addTest(Test_download('test_homepage'))
	#suite.addTest(Test_download('test_login'))
	runner=unittest.TextTestRunner()
	runner.run(suite)
