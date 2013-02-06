"""provide interface to download data of a certain pageStyle of someone from www.renren.com"""
import urllib.request
from urllib.parse import urlencode
import http.cookiejar

import socket

import re
import time

import parse

timeout=3
urls={
	'login':"http://www.renren.com/PLogin.do",
	'friendList':"http://friend.renren.com/GetFriendList.do?curpage={}&id={}",
	'profile_detail':"http://www.renren.com/{}/profile?v=info_ajax",
	'status':'http://status.renren.com/status?curpage={}&id={}&__view=async-html',
	'homepage':"http://www.renren.com/{}/profile"}
itemReg={
	'status':re.compile(r'<li data-wiki = "" id="status-\d+">.*?</li>',re.DOTALL),
	'friendList':re.compile(r'<dd><a\s+href="http://www.renren.com/profile.do\?id=\d+">[^<]*</a>'),
	'profile_detail':re.compile(r'<dl\sclass="info">.*?</dl>',re.DOTALL),
	'profile_tl':re.compile(r'<ul class="information-ul".*?</ul>',re.DOTALL),
	'profile_basic':re.compile(r'<ul class="user-info clearfix">.*?</ul>',re.DOTALL)}
	#'homepage_basic':re.compile(r'<(?:u|d)l class="(?:user-info )*?clearfix">.*?</(?:u|d)l>',re.DOTALL)}

def format_timecost(timecost):
	if isinstance(timecost,list):
		import numpy as np
		tm=np.float32(timecost)
		return 'max/min/ave:%.2f/%.2f/%.2f'%(tm.max(),tm.min(),tm.mean())
	else:
		return 'timecost format error'

class download:
	_request_time=list()

	def __init__(self,user='yyttrr3242342@163.com',passwd=None):
		if passwd is None:
			import mytools #used to get passwd from personal mysql
			passwd=mytools.getPasswd('renren',user)
		renrenId,detail=self.login(user,passwd)
		if renrenId is None:
			print('login failed,user={},{}'.format(user,detail))
		#socket.setdefaulttimeout(timeout)

	def friendList(self,renrenId='285060168',uppage=100):
		"""friendList('285060168') --> 
		return {friend_rid1:name1,friend_rid2:name2} in the page,
		return dict() if forbidden by privacy policy
		log error and return correct items, if timeout or parse error"""
		pageStyle='friendList'
		hrefs,timecost=self.iterPage(pageStyle,renrenId,uppage)
		return parse.friendList(hrefs),timecost
	def status(self,renrenId='285060168',uppage=100):
		"""status('285060168') --> 
		(statusId,cur_content,orig_content,timestamp)"""
		pageStyle='status'
		stat,timecost=self.iterPage(pageStyle,renrenId,uppage)
		return parse.status(stat),timecost

	def profile(self,renrenId):
		"""profile('234234') -->
		return {tag1:value1,...,tagn:valuen} in detail page if available
		return {tag1:value1,...,tagn:valuen} in homepage if detail page unavailable
		return None if timeout"""
		pageStyle='profile_detail'
		html_content=self.onePage(urls[pageStyle].format(renrenId))
		if html_content is None:
			return None,None
		elif html_content[0:30].find('<div class="col-left">') > -1:
			return 'detail',parse.profile_detail(itemReg[pageStyle].findall(html_content))
		elif html_content[0:30].find('<!doctype html><html>') > -1:#tl
			return 'mini_tl',parse.homepage_tl(itemReg['profile_tl'].findall(html_content))
		else:
			return 'mini_basic',parse.homepage_basic_privacy(itemReg['profile_basic'].findall(html_content))

	def homepage(self,renrenId):
		pageStyle='homepage'
		html_content=self.onePage(urls[pageStyle].format(renrenId))
		if html_content is None:
			return set()
		elif html_content[0:30].find('<!doctype html><html>') > -1:#tl
			return parse.homepage_tl(itemReg[pageStyle+'_tl'].findall(html_content))
		else:
			return parse.homepage_basic(itemReg[pageStyle+'_basic'].findall(html_content))

	def onePage(self,url,request_time=None):
		"""onePage(url) --> 
		return html_content if success
		return None if timeout.
		write request_time in _request_time
		"""
		try:
			if request_time is not None:
				request_start=time.time()
			rsp=self.opener.open(url,timeout=timeout)
			html_content=rsp.read().decode('UTF-8','ignore')
			if request_time is not None:
				request_time.append(time.time()-request_start)
		except socket.timeout as e:
			return None
		except urllib.error.URLError as e:
			return None
		else:
			return html_content

	def iterPage(self,pageStyle=None,renrenId=None,uppage=100,log=None):
		"""iterPage(pageStyle,renrenId)  --> 
		return set(items),timecost if success,
		return set(),timecost if forbidden by privacy policy,
		return None,timecost if timeout."""
		itemsAll=set()
		timeout_list=list()
		req_time=list()
		runtime_start=time.time()
		#request and parse pages
		for curpage in range(uppage):
			html_content=self.onePage(urls[pageStyle].format(curpage,renrenId),req_time)
			if html_content is None:#if timeout, log error to resend later.
				timeout_list.append(curpage)
			else:
				items_curpage=itemReg[pageStyle].findall(html_content)
				if len(items_curpage) < 1:#privacy/all pages requested.
					break
				else:
					itemsAll=itemsAll | set(items_curpage)
		#resend timeout_list
		for page in timeout_list:
			html_content=self.onePage(urls[pageStyle].format(page,renrenId))
			if html_content is None:
				return None
			else:
				items_curpage=itemReg[pageStyle].findall(html_content)
				itemsAll=itemsAll | set(items_curpage)
		#timecost
		runtime=time.time()-runtime_start
		#data check
		#request last page and check by number of datas
		return itemsAll,'time={},{}'.format(format(runtime,'.2f'),format_timecost(req_time))

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
		except socket.timeout as e:
			return None,'timeout'
		except urllib.error.URLError as e:
			return None
		else:
			#check whether login is successful. 
			m=re.compile(r'http://www.renren.com/(\d+)').match(url)
			if m is None:
				return None,'login failed,rsp={}'.format(url)
			else:
				return m.group(1),'success'

		if _err is not set():
			print('error:{}'.format(_err))
