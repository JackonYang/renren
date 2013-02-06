
import unittest
from download import download

_url2fileprog=None
def url2file(url):
	global _url2fileprog
	if _url2fileprog is None:
		import re
		_url2fileprog=re.compile(r'http://(\w+).renren.com/(?:\D+)?(\d+)\D+(\d+)?')
	m=_url2fileprog.search(url)
	if m is None:
		return None
	else:
		if m.group(3) is None:
			return 'test_data/{}_{}_profile.html'.format(m.group(1),m.group(2))
		else:
			return 'test_data/{}_{}_{}.html'.format(m.group(1),m.group(2),m.group(3))

class newDownload(download):
	def __init__(self):
		download.__init__(self,None)#no auto login
	def onePage(self,url,request_time=None):
		try:
			f=open(url2file(url),'r')
			html_content=str(f.readlines())
			f.close()
		except Exception as e:
			return None
		if request_time is not None:
			request_time.append(1.11)#random time
		return html_content

class Test_download(unittest.TestCase):
	def setUp(self):
		pass

	def test_newDownload(self):
		new_dl=newDownload()
		request_time=[]
		new_dl.onePage('http://www.renren.com/233330059/profile',request_time)
		print(request_time)
		print(new_dl.iterPage('friendList','439682367'))

	def tearDown(self):
		pass

	def test_profile(self):
		renrenIds={'233330059','230760442','223981104','410941086','285060168'}
							#myself,timeline ok/unavailable,old style ok/unavailable
		for rid in renrenIds:
			pfStyle,details=self.dl.profile(rid)
			print('{},{},{}'.format(rid,pfStyle,details))

	def test_friendList(self):
		renrenIds={'233330059','410941086','267654044','285060168','240303471'}
							#myself,3+pages/2pages/1page/unavailable
		for rid in renrenIds:
			fl,timecost=self.dl.friendList(rid)
			if isinstance(fl,dict):
				print('{},{},{}'.format(rid,len(fl),timecost))
			else:
				print('error.interface specification')

	def test_status(self):
		#renrenIds={'233330059','410941086','267654044','285060168','240303471'}
		renrenIds={'410941086','284874220'}
		for rid in renrenIds:
			stat,timecost=self.dl.status(rid)
			#print('{},{},{}'.format(rid,len(stat),timecost))
			print('{},{},{}'.format(rid,stat,timecost))

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
	#suite.addTest(Test_download('test_status'))
	#suite.addTest(Test_download('test_profile'))
	#suite.addTest(Test_download('test_homepage'))
	#suite.addTest(Test_download('test_login'))
	suite.addTest(Test_download('test_newDownload'))
	
	runner=unittest.TextTestRunner()
	runner.run(suite)
