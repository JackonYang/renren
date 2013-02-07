import unittest
import browser

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

class newBrowser(browser.browser):
	def __init__(self):
		browser.__init__(self)#no auto login
	def _one_page(self,url,request_time=None):
		f=open(url2file(url),'r')
		try:
			html_content=str(f.readlines())
		except Exception as e:
			f.close()
			print(e)
			return None
		f.close()
		if request_time is not None:
			request_time.append(1.11)#random time
		return html_content

class Test_browser(unittest.TestCase):
	def setUp(self):
		pass
		#self.dl=newDownload()

	def test_newBrowser(self):
		new_dl=newBrowser()
		#request_time=[]
		#new_dl.onePage('http://www.renren.com/233330059/profile',request_time)
		#print(request_time)
		#print(new_dl.iterPage('friendList','439682367'))

	def tearDown(self):
		pass

	def test_profile(self):
		renrenIds={'233330059','230760442','223981104','410941086','285060168'}
							#myself,timeline ok/unavailable,old style ok/unavailable
		for rid in renrenIds:
			pfStyle,details=self.dl.profile(rid)
			print('{},{},{}'.format(rid,pfStyle,details))

	def test_friendList(self):
		#page sequence 3+pages/2pages/1page
		correct_seq={'410941086':178,'267654044':29,'285060168':5}
		for rid,expt in correct_seq.items():
			fl,timecost=self.dl.friendList(rid)
			self.assertEquals(len(fl),expt)
			self.assertTrue(timecost.find('max/min/ave')>-1)
		#privacy
		rid='240303471'
		expt=0
		fl,timecost=self.dl.friendList(rid)
		self.assertEquals(len(fl),0)
		self.assertTrue(timecost.find('max/min/ave')>-1)
		#timeout:1page/2page/all pages timeout
		#content/some items parse error

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

	def test_download(self):
		dl=browser.browser()
		dl.login('test','test')
		url_normal="http://www.baidu.com"
		self.assertTrue(isinstance(dl._download(url_normal),str))
		url_timeout="http://1.1.1.1"
		self.assertEquals(dl._download(url_timeout),None)

	def test_login(self):
		users=[
				('jiekunyang@gmail.com','233330059'),
				('zhangxiaoxu_521@yahoo.com.cn','410941086'),
				('yyttrr3242342@163.com','498934189')
				]
		#each account login only once to avoid safety policy
		#istance user
		user,expt=users[0]
		dl=browser.browser(user)
		rid,info=dl.login()
		self.assertEquals(rid,expt)
		#explict login
		user,expt=users[1]
		dl=browser.browser(user)
		rid,info=dl.login(user)
		self.assertEquals(rid,expt)
		#explict and wrong passwd
		user,expt=users[2]
		dl=browser.browser(user)
		rid,info=dl.login(user,'error')
		self.assertEquals(rid,None)
		#instance passwd wrong, but login explict with correct passwd
		dl=browser.browser(user,'error')
		rid,info=dl.login(user)
		self.assertEquals(rid,expt)

if __name__=='__main__':
	suite=unittest.TestSuite()
	#suite.addTest(Test_browser('test_friendList'))
	#suite.addTest(Test_browser('test_status'))
	#suite.addTest(Test_browser('test_profile'))
	#suite.addTest(Test_browser('test_homepage'))
	#suite.addTest(Test_browser('test_newDownload'))

	suite.addTest(Test_browser('test_download'))
	#checked
	#suite.addTest(Test_browser('test_login'))
	
	runner=unittest.TextTestRunner()
	runner.run(suite)
