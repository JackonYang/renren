"""download data from www.renren.com"""
import urllib.request
from urllib.parse import urlencode
import http.cookiejar

import re
import time

timeout=3
urls={
	'login':"http://www.renren.com/PLogin.do",
	'friendList':"http://friend.renren.com/GetFriendList.do?curpage={}&id={}",
	'profile_detail':"http://www.renren.com/{}/profile?v=info_ajax",
	'status':'http://status.renren.com/status?curpage={}&id={}&__view=async-html',
	'homepage':"http://www.renren.com/{}/profile"}
itemReg={
	'status':r'id="status-.+?ilike_icon',
	'friendList':re.compile(r'<dd><a\s+href=\"http://www.renren.com/profile.do\?id=\d+\">.+?<\/a>'),
	'profile_detail':re.compile(r'<dl\sclass="info">.*?</dl>',re.DOTALL),
	'homepage_tl':re.compile(r'<ul class="information-ul".*?</ul>',re.DOTALL),
	'homepage_basic':re.compile(r'<(?:u|d)l class="(?:user-info )*?clearfix">.*?</(?:u|d)l>',re.DOTALL)}

class download:

	def __init__(self,user='yyttrr3242342@163.com',passwd=None):
		if passwd is None:
			import mytools #used to get passwd from personal mysql
			passwd=mytools.getPasswd('renren',user)
		renrenId,reason=self.login(user,passwd)
		if renrenId is None:
			print('login failed,user={},{}'.format(user,reason))

	def friendList(self,renrenId='285060168',targetPage=None, uppage=100):
		"""friendList('234234') -->
		return (friendList,info) if success
		return (set(),'privacy') if can't access because of privacy policy
		return (set(),info) if some pages parse error
		return (set(),'timeout') if timeout"""
		pageStyle='friendList'
		if targetPage==None:
			return self.iterPage(pageStyle,renrenId,uppage)
		else:
			return self.onePage(urls[pageStyle].format(curpage,renrenId))
			#parse

	def status(self,renrenId=None,targetPage=None, uppage=100):
		pageStyle='status'
		if targetPage==None:
			return self.iterPage(pageStyle,renrenId,uppage)
		else:
			return self.onePage(urls[pageStyle].format(curpage,renrenId))

	def profile_detail(self,renrenId):
		"""profile_detail('234234') -->
		return (items,'success') if success
		return (set(),'privacy') if can't access because of privacy policy
		return (set(),'timeout') if timeout"""
		pageStyle='profile_detail'
		html_content,info=self.onePage(urls[pageStyle].format(renrenId))
		if html_content is None:
			return set(),info
		elif html_content[0:30].find('<div class="col-left">') > -1:
			items_curpage=itemReg[pageStyle].findall(html_content)
			return items_curpage,'success'
		else:
			return set(),'privacy'

	def homepage(self,renrenId):
		pageStyle='homepage'
		html_content,info=self.onePage(urls[pageStyle].format(renrenId))
		if html_content is None:
			return set(),info
		elif html_content[0:30].find('<!doctype html><html>') > -1:#tl
			items_curpage=itemReg[pageStyle+'_tl'].findall(html_content)
			return items_curpage,'tl'
		else:
			items_curpage=itemReg[pageStyle+'_basic'].findall(html_content)
			return items_curpage,'basic'

	def onePage(self,url):
		try:
			rsp=self.opener.open(url)
			#rspurl=rsp.geturl()
			html_content=rsp.read().decode('UTF-8','ignore')
		except urllib.error.URLError as e:
			return None,'timeout'
		#TODO: deal with resend
		else:
			return html_content,'success'

	def iterPage(self,pageStyle=None,renrenId=None,uppage=100):
		itemsAll=set()
		request_time=[]
		for curpage in range(uppage):
			request_start=time.time()
			html_content,info=self.onePage(urls[pageStyle].format(curpage,renrenId))
			request_time.append(time.time()-request_start)
			if html_content is None:
				return set(),info
			else:
				items_curpage=itemReg[pageStyle].findall(html_content)
				if len(items_curpage) < 1:#all pages request
					if html_content.find('f-privacy-tip')>0:
						return set(),'privacy'
					break
				else:
					itemsAll=itemsAll | set(items_curpage)
					last_num=len(items_curpage)

		#check data
		if len(itemsAll) == 20*curpage-20+last_num:#success
			#return itemsAll,'timecost:{}/{}/{}(max/min/ave)'.format(0,0,0)
			return itemsAll,'timecost:{}'.format(request_time)
		else:
			return set(),'parse error.expt={},actual={}'.format(curpage*20-20+n,len(itemsAll))

	def login(self,user,passwd):
		"""return (renrenId,'success') if login successfully.
		return (None,reason) if failed."""
		data=urlencode({"email":user,"password":passwd}).encode(encoding='UTF8');
		hdlr_cookie=urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar())
		self.opener=urllib.request.build_opener(hdlr_cookie)
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
				return None,'login failed,rsp={}'.format(url)
			else:
				return m.group(1),'success'
