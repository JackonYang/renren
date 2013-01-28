import unittest
import parse
from download import download

pfHrefs=[
	{'<dd><a href="http://www.renren.com/profile.do?id=6754031">王瑛</a>',
	'<dd><a href="http://www.renren.com/profile.do?id=331442">En.王哲</a>'},
	{'<dd><a href="http://www.renren.com/profile.do?id=9439171"></a>'},
	'<dd><a href="http://www.renren.com/profile.do?id=34134">～@%……</a>',
	{'error'}]
names=[
	{'6754031':'王瑛','331442':'En.王哲'},
	{'9439171':''},
	{'34134':'～@%……'},
	None]


class Test_parse(unittest.TestCase):

	def setUp(self):
		user='jiekunyang@gmail.com'
		self.dl=download(user)
	def tearDown(self):
		pass

	def test_profile_detail(self):
		renrenIds={'233330059','230760442','223981104','410941086','285060168','241331952','294126602','239486743'}
							#myself,timeline ok/unavailable,old style ok/unavailable
		for rid in renrenIds:
			info,reason=self.dl.profile_detail(rid)
			print('{},{}'.format(rid,reason))
			#print(info)
			print(parse.profile_detail(info))

	def test_friendList(self):
		for pfHref,name in zip(pfHrefs,names):
			self.assertEquals(parse.friendList(pfHref),name)

	def test_homepage(self):
		renrenIds={'233330059','410941086','267654044','285060168','240303471'}
		for rid in renrenIds:
			info,reason=self.dl.homepage(rid)
			print('{},{},{}'.format(rid,len(info),reason))

	def test_login(self):
		users=['yyttrr3242342@163.com','jiekunyang@gmail.com','zhangxiaoxu_521@yahoo.com.cn','none@adaf.com']
		rids=['498934189','233330059','410941086',None]
		for user,rid in zip(users,rids):
			dl=download(user)

if __name__=='__main__':
	suite=unittest.TestSuite()
	#suite.addTest(Test_parse('test_friendList'))
	suite.addTest(Test_parse('test_profile_detail'))
	#suite.addTest(Test_parse('test_homepage'))
	#suite.addTest(Test_parse('test_login'))
	runner=unittest.TextTestRunner()
	runner.run(suite)
