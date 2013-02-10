import unittest
import browser

class new_browser(browser.browser):
	def __init__(self):
		browser.browser.__init__(self)#no auto login
		self.dl=None#used by get_test_data() to download data from renren.com
		self.sent_times=dict()#used to test for timeout and resend
	def _download(self,url,request_time=None):
		filename='{}{}'.format(browser.url2file(url),self.sent_times.get(url,''))
		self.sent_times[url] = self.sent_times.get(url,0)+1
		try:
			html_content=''.join([line for line in open(filename)])
		except IOError as e:#simulate timeout
			html_content=None
		if request_time is not None:
			request_time.append(1.11)#random time
		return html_content
	def get_test_data(self,pageStyle,rid,uppage=110):
		if self.dl is None:
			self.dl=browser.browser('jiekunyang@gmail.com')
			self.dl.login()
		meth=getattr(browser.browser,pageStyle)
		browser.run_level='debug'
		meth(self.dl,rid,uppage)
		browser.run_level='info'
	def flush_test_data(self):#used to test timeout and resend
		self.sent_times=dict()
		#print('data flushed')

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
		#normal seq, privacy
		dl=new_browser()
		dl.login('test','test')
		test_data={'240303471':0,'446766202':1,'500275848':2,'444024948':20,'384065413':21,'397529849':22,'739807017':40}
		for rid,expt in test_data.items():
			record,timecost=dl.friendList(rid)
			self.assertEquals(len(record),expt)
			self.assertTrue(isinstance(record,dict))
			self.assertTrue(timecost.find('max/min/ave')>-1)
		#error info test
		error_data={'99999999':'more timeout than max_timeout','9999998':'timeout'}
		for rid,expt in error_data.items():
			record,info=dl.friendList(rid)
			self.assertEquals(record,None)
			self.assertTrue(info,expt)

	def test_status(self):
		dl=new_browser()
		dl.login('test','test')
		test_data={'446766202':0,'500275848':1,'104062077':2,'232877604':20,'242641331':21,'256137627':22,'411984911':40}
		for rid,expt in test_data.items():
			record,timecost=dl.status(rid)
			self.assertEquals(len(record),expt)
			self.assertTrue(isinstance(record,dict))
			self.assertTrue(timecost.find('max/min/ave')>-1)
		#error info test
		error_data={'99999999':'more timeout than max_timeout','9999998':'timeout'}
		for rid,expt in error_data.items():
			record,info=dl.status(rid)
			self.assertEquals(record,None)

	def test_iter_page(self):
		"""focus on page sequence"""
		dl=new_browser()
		dl.login('test','test')
		#page sequence 2pages/1page/0page,items in end page, 1/2/20
		friendList={'240303471':0,'446766202':1,'500275848':2,'444024948':20,'384065413':21,'397529849':22,'739807017':40}
		status={'446766202':0,'500275848':1,'104062077':2,'232877604':20,'242641331':21,'256137627':22,'411984911':40}
		for rid,expt in friendList.items():
			items,info=dl._iter_page('friendList',rid)
			self.assertEquals(len(items),expt)
			self.assertEquals(info,'success')
		for rid,expt in status.items():
			items,info=dl._iter_page('status',rid)
			self.assertEquals(len(items),expt)
			self.assertEquals(info,'success')
		#more page than expt
		over={'287286312':'friendList','259364921':'status'}
		uppage=105
		for rid,pageStyle in over.items():
			items,info=dl._iter_page(pageStyle,rid,None,range(0,uppage))
			self.assertEquals(len(items),2100)
			self.assertEquals(info,'success')

	def test_iter_page_timeout(self):
		"""timeout:1page/several page but less than max_timeout/more than normal/all pages"""
		dl=new_browser()
		dl.login('test','test')
		dl.flush_test_data()
		pageStyle='friendList'
		#all timeout
		rid='99999999'
		items,info=dl._iter_page(pageStyle,rid)
		self.assertEquals(items,None)
		self.assertEquals(info,'more timeout than max_timeout')
		dl.flush_test_data()
		#one page timeout and resend ok
		rid='99990001'
		browser.resend_n=0#close resend
		items,info=dl._iter_page(pageStyle,rid)
		self.assertEquals(items,None)
		self.assertEquals(info,'timeout')
		dl.flush_test_data()
		browser.resend_n=1#resend once
		items,info=dl._iter_page(pageStyle,rid)
		self.assertEquals(len(items),20)
		self.assertEquals(info,'success')
		dl.flush_test_data()
		#more timeout than normal,stop immediately and return None .
		rid='119815062'
		browser.max_timeout=5
		items,info=dl._iter_page(pageStyle,rid)
		self.assertEquals(items,None)
		self.assertEquals(info,'more timeout than max_timeout')
		dl.flush_test_data()
		#several timeout but less than max_timeout,resend ok
		browser.max_timeout=10
		browser.resend_n=3#resend 3 times
		items,info=dl._iter_page(pageStyle,rid)
		self.assertEquals(len(items),170)
		self.assertEquals(info,'success')

	def test_iter_page_safety(self):
		#fist page,middle page
		#TODO:need safety page
		rids=[99991001,99991002]
		dl=new_browser()
		dl.login('test','test')
		pageStyle='friendList'
		for rid in rids:
			self.assertEquals(dl._iter_page(pageStyle,rid),None)


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
		items,info=dl._iter_page('friendList','287286312',request_time,range(0,10))#10 more timecost info
		self.assertTrue(isinstance(items,set))#10 more timecost info
		self.assertEquals(info,'success')#10 more timecost info
		self.assertEquals(len(request_time),11)
		self.assertEquals(dl._download('http://1.1.1.1'),None)
		self.assertTrue(isinstance(dl._download('http://1.1.1.1'),str))

if __name__=='__main__':
	suite=unittest.TestSuite()
	#suite.addTest(Test_browser('test_profile'))
	#suite.addTest(Test_browser('test_homepage'))

	#TODO:no test data file
	#suite.addTest(Test_browser('test_is_safety_page'))

	#checked
	#suite.addTest(Test_browser('test_login'))
	#suite.addTest(Test_browser('test_download'))
	suite.addTest(Test_browser('test_new_browser'))
	suite.addTest(Test_browser('test_iter_page'))
	suite.addTest(Test_browser('test_iter_page_timeout'))
	suite.addTest(Test_browser('test_friendList'))
	suite.addTest(Test_browser('test_status'))
	
	runner=unittest.TextTestRunner()
	runner.run(suite)
