import unittest
import browser

class new_browser(browser.browser):
	def __init__(self):
		browser.browser.__init__(self)#no auto login
		self.dl=None
	def _download(self,url,request_time=None):
		filename=browser.url2file(url)
		try:
			html_content=''.join([line for line in open(filename)])
		except IOError as e:#simulate timeout
			html_content=None
		if request_time is not None:
			request_time.append(1.11)#random time
		return html_content
	def get_test_data(self,pageStyle,rid):
		if self.dl is None:
			self.dl=browser.browser('jiekunyang@gmail.com')
			self.dl.login()
		meth=getattr(browser.browser,pageStyle)
		browser.run_level='debug'
		meth(self.dl,rid)
		browser.run_level='info'

class Test_browser(unittest.TestCase):
	def setUp(self):
		pass
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

	def test_iter_page(self):
		"""focus on page sequence"""
		dl=new_browser()
		dl.login('test','test')
		#page sequence 2pages/1page/0page
		#items in end page, 1/2/20
		friendList={'240303471':0,'446766202':1,'500275848':2,'444024948':20,'384065413':21,'397529849':22,'739807017':40}
		#status={'446766202':0,'500275848':2
		for rid,expt in friendList.items():
			self.assertEquals(len(dl._iter_page('friendList',rid)),expt)
		#page more than expt
		over={'287286312','friendList'}
		self.assertEquals(len(dl._iter_page('friendList',rid)),2000)

		#self.assertEquals(len(fl),0)
		#self.assertTrue(timecost.find('max/min/ave')>-1)
		#timeout:1page/2page/all pages timeout
		#1+ pages which is not filled with items

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
		self.assertTrue(isinstance(dl._download(url_timeout),str))

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

	def test_new_browser(self):
		dl=new_browser()
		request_time=[]
		self.assertEquals(dl._download('http://1.1.1.1',request_time),None)
		self.assertEquals(len(request_time),1)
		self.assertTrue(isinstance(dl._download('http://friend.renren.com/GetFriendList.do?curpage=0&id=240303471'),str))
		self.assertEquals(len(request_time),1)
		self.assertTrue(isinstance(dl._iter_page('friendList','287286312',request_time,range(0,10)),set))#10 more timecost info
		self.assertEquals(len(request_time),11)

if __name__=='__main__':
	suite=unittest.TestSuite()
	#suite.addTest(Test_browser('test_friendList'))
	#suite.addTest(Test_browser('test_status'))
	#suite.addTest(Test_browser('test_profile'))
	#suite.addTest(Test_browser('test_homepage'))

	#suite.addTest(Test_browser('test_iter_page'))

	#checked
	#suite.addTest(Test_browser('test_login'))
	#suite.addTest(Test_browser('test_download'))
	#suite.addTest(Test_browser('test_new_browser'))
	
	runner=unittest.TextTestRunner()
	runner.run(suite)
