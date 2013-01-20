"""download data from www.renren.com"""
import urllib.request
from urllib.parse import urlencode
import http.cookiejar

import re
import time

import mytools #used to get passwd from personal mysql

timeout=3
urls={
	'status':'http://status.renren.com/status?curpage={}&id={}&__view=async-html',
	'friendList':"http://friend.renren.com/GetFriendList.do?curpage={}&id={}",
	'profile_info':"http://www.renren.com/{}/profile?v=info_ajax",
	'login':"http://www.renren.com/PLogin.do"}

class download:
	itemReg={
		'status':r'id="status-.+?ilike_icon',
		'friendList':re.compile(r'<dd><a\s+href=\"http://www.renren.com/profile.do\?id=\d+\">.+?<\/a>'),
		'profile_info':re.compile(r'<dl\sclass="info">.*?</dl>',re.DOTALL)}

	def __init__(self,user='yyttrr3242342@163.com',passwd=None):
		if passwd is None:
			passwd=mytools.getPasswd('renren',user)
		renrenId,reason=self.login(user,passwd)
		if renrenId is None:
			print('login failed,user={},{}'.format(user,reason))

	def friendList(self,renrenId='285060168',targetPage=None, uppage=100):
		"""friendList('234234') -->
		return friendList,timecost:total/download/perpage if success
		return set(),privacy if can't access because of privacy policy
		return set(),expt={},actual={} if some pages parse error"""
		pageStyle='friendList'
		if targetPage==None:
			return self.iterPage(pageStyle,renrenId,uppage)
		else:
			return self.onePage(urls[pageStyle].format(curpage,renrenId))

	def status(self,renrenId=None,targetPage=None, uppage=100):
		pageStyle='status'
		if targetPage==None:
			return self.iterPage(pageStyle,renrenId,uppage)
		else:
			return self.onePage(urls[pageStyle].format(curpage,renrenId))

	def profile(self,renrenId):
		pageStyle='profile_info'
		html_content,time=self.onePage(urls[pageStyle].format(renrenId))
		if html_content is None:
			print(time)
			return set(),'timeout'
		elif html_content[0:30].find('<div class="col-left">')==-1:
			return set(),'privacy'
		else:
			#parse
			items_curpage=self.itemReg[pageStyle].findall(html_content)
			return items_curpage,'success'

	def onePage(self,url):
		startTime=time.time()
		try:
			rsp=self.opener.open(url)
			htmlStr=rsp.read().decode('UTF-8','ignore')
		except urllib.error.URLError as e:
			return None,'timeout'
		#TODO: deal with resend
		else:
			stopTime=time.time()
			return htmlStr,stopTime-startTime

	def iterPage(self,pageStyle=None,renrenId=None,uppage=100):
		looptime=0
		start=time.time()
		itemsAll=set()
		for curpage in range(uppage+1):
			html_content,timecost=self.onePage(urls[pageStyle].format(curpage,renrenId))
			if html_content is None:
				return set(),'{} ,page={},renrenId={},{}.'.format(pageStyle,curpage,renrenId,timecost)
			else:
				items_curpage=self.itemReg[pageStyle].findall(html_content)
			if len(items_curpage) < 1:#all pages request
				stop=time.time()
				if html_content.find('f-privacy-tip')>0:
					return set(),'privacy'
				break
			else:
				looptime += timecost
				n=len(items_curpage)
				itemsAll=itemsAll | set(items_curpage)
		#check data
		if len(itemsAll) == 20*curpage-20+n:#success
			return itemsAll,'timecost:{}/{}/{}(total/download/perpage)'.format(stop-start,looptime,looptime/curpage)
		else:
			return {},'parse error.expt={},actual={}'.format(curpage*20-20+n,len(itemsAll))

	def login(self,user,passwd):
		"""return renrenId and set build default opener if login successfully.
		return None if failed."""
		data=urlencode({"email":user,"password":passwd}).encode(encoding='UTF8');
		cj=http.cookiejar.CookieJar();
		self.opener=urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj));
		self.opener.addheaders=[('User-agent','Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0')];
		try:
			rsp=self.opener.open(urls['login'],data,timeout=timeout)
			url=rsp.geturl()
		except urllib.error.URLError as e:
			return None,'timeout'
		else:
			#check whether login is successful. 
			m=re.compile(r'http://www.renren.com/(\d+)').match(url)
			if m is None:
				return None,url
			else:
				return m.group(1),'success'

