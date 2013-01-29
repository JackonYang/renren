"""download data from www.renren.com"""
import urllib.request
from urllib.parse import urlencode
import http.cookiejar

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
	'status':r'id="status-.+?ilike_icon',
	'friendList':re.compile(r'<dd><a\s+href=\"http://www.renren.com/profile.do\?id=\d+\">.+?<\/a>'),
	'profile_detail':re.compile(r'<dl\sclass="info">.*?</dl>',re.DOTALL),
	'homepage_tl':re.compile(r'<ul class="information-ul".*?</ul>',re.DOTALL),
	'homepage_basic':re.compile(r'<(?:u|d)l class="(?:user-info )*?clearfix">.*?</(?:u|d)l>',re.DOTALL)}

err=set()
def _error(info):
	err.add(info)

timecost=dict()
def _log_time(url,time):
	timecost[url]=time

class download:

	def __init__(self,user='yyttrr3242342@163.com',passwd=None):
		if passwd is None:
			import mytools #used to get passwd from personal mysql
			passwd=mytools.getPasswd('renren',user)
		renrenId,reason=self.login(user,passwd)
		if renrenId is None:
			print('login failed,user={},{}'.format(user,reason))

	def friendList(self,renrenId='285060168',targetPage=None, uppage=100):
		"""friendList('285060168') --> 
		return {friend_rid1:name1,friend_rid2:name2} if success
		return dict{} if can't access because of privacy policy, pages parse error, or timeout"""
		pageStyle='friendList'
		if targetPage==None:
			hrefs=self.iterPage(pageStyle,renrenId,uppage)
		else:
			hrefs=self.onePage(urls[pageStyle].format(curpage,renrenId))
		return parse.friendList(hrefs)

	def status(self,renrenId=None,targetPage=None, uppage=100):
		pageStyle='status'
		if targetPage==None:
			return self.iterPage(pageStyle,renrenId,uppage)
		else:
			return self.onePage(urls[pageStyle].format(curpage,renrenId))

	def profile_detail(self,renrenId):
		"""profile_detail('234234') -->
		return items if success
		return set() if can't access because of privacy policy or timeout"""
		pageStyle='profile_detail'
		html_content=self.onePage(urls[pageStyle].format(renrenId))
		if html_content is None:
			return dict()
		elif html_content[0:30].find('<div class="col-left">') > -1:
			return parse.profile_detail(itemReg[pageStyle].findall(html_content))
		else:
			_error('{},{},privacy'.format(renrenId,pageStyle))
			return dict()

	def homepage(self,renrenId):
		pageStyle='homepage'
		html_content=self.onePage(urls[pageStyle].format(renrenId))
		if html_content is None:
			return set()
		elif html_content[0:30].find('<!doctype html><html>') > -1:#tl
			return parse.homepage_tl(itemReg[pageStyle+'_tl'].findall(html_content))
		else:
			return parse.homepage_basic(itemReg[pageStyle+'_basic'].findall(html_content))

	def onePage(self,url):
		try:
			request_start=time.time()
			rsp=self.opener.open(url)
			html_content=rsp.read().decode('UTF-8','ignore')
			_log_time(url,time.time()-request_start)
		except urllib.error.URLError as e:
			#TODO: deal with resend
			_error('{}----{}'.format(url,'timeout'))
			return None
		else:
			return html_content

	def iterPage(self,pageStyle=None,renrenId=None,uppage=100):
		itemsAll=set()
		request_time=[]
		for curpage in range(uppage):
			html_content=self.onePage(urls[pageStyle].format(curpage,renrenId))
			if html_content is not None:#if timeout,go on with next page
				items_curpage=itemReg[pageStyle].findall(html_content)
				if len(items_curpage) < 1:#all pages parsed
					break
				else:
					itemsAll=itemsAll | set(items_curpage)
					last_num=len(items_curpage)
		if html_content.find('f-privacy-tip')>0:
			_error('{},{},privacy'.format(renrenId,pageStyle))
		elif len(itemsAll) != 20*curpage-20+last_num:
			_error('parse error.expt={},actual={}'.format(curpage*20-20+last_num,len(itemsAll)))
		return itemsAll

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

	def out_timecost(self):
		global timecost
		import numpy as np
		tm=np.float32(list(timecost.values()))
		print('max/min/ave:{}/{}/{}.'.format(tm.max(),tm.min(),tm.mean()))
		timecost=dict()
	def out_err(self):
		print(err)
