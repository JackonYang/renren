import unittest
from download import download

class Test_download(unittest.TestCase):

	def setUp(self):
		pass
		#self.browser.login()
	def tearDown(self):
		pass

	def testProfile(self):
		renrenIds={'233330059','230760442','223981104','410941086','285060168'}
							#myself,timeline ok/unavailable,old style ok/unavailable
		self.browser.setLogLevel(10)#debug

		self.browser.localSave(False)
		for renrenId in renrenIds:
			self.assertNotEqual(self.browser.profile(renrenId),'timeout')
		self.assertFalse(os.path.exists(self.pwdSave))#path not exist

		self.browser.localSave(True)
		for renrenId in renrenIds:
			self.assertNotEqual(self.browser.profile(renrenId),'timeout')
		self.assertEqual(len(os.listdir(self.pwdSave)),len(renrenIds))

	def test_friendList(self):
		user='yyttrr3242342@163.com'
		dl=download(user)
		renrenIds={'233330059','410941086','267654044','285060168','240303471'}
							#myself,3+pages/2pages/1page/unavailable
		for rid in renrenIds:
			fl,reason=dl.friendList(rid)
			print('{},{},{}'.format(rid,len(fl),reason))
		#flist={'232639310':35,'242543024':152,'285060168':5}
		#for item in flist.items():
			#self.assertEqual(len(self.browser.friendList(item[0])),item[1])

	def test_login(self):
		users=['yyttrr3242342@163.com','jiekunyang@gmail.com','zhangxiaoxu_521@yahoo.com.cn','none@adaf.com']
		rids=['498934189','233330059','410941086',None]
		for user,rid in zip(users,rids):
			dl=download(user)

if __name__=='__main__':
	suite=unittest.TestSuite()
	#suite.addTest(TestRenrenBrowser('testProfile'))
	suite.addTest(Test_download('test_friendList'))
	suite.addTest(Test_download('test_login'))
	runner=unittest.TextTestRunner()
	runner.run(suite)
