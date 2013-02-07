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
	'homepage':"http://www.renren.com/{}/profile",
	'status':'http://status.renren.com/status?curpage={}&id={}&__view=async-html'
	}
itemReg={
	'status':re.compile(r'<li data-wiki = "" id="status-\d+">.*?</li>',re.DOTALL),
	'friendList':re.compile(r'<dd><a\s+href="http://www.renren.com/profile.do\?id=\d+">[^<]*</a>'),
	'profile_detail':re.compile(r'<dl\sclass="info">.*?</dl>',re.DOTALL),
	'profile_tl':re.compile(r'<ul class="information-ul".*?</ul>',re.DOTALL),
	'safety':re.compile(r'<title>.*?安全.*?</title>'),
	'profile_basic':re.compile(r'<ul class="user-info clearfix">.*?</ul>',re.DOTALL)}
	#'homepage_basic':re.compile(r'<(?:u|d)l class="(?:user-info )*?clearfix">.*?</(?:u|d)l>',re.DOTALL)}

def format_time(runtime,req_time):
	if isinstance(req_time,list):
		import numpy as np
		tm=np.float32(req_time)
		return '%.2f,max/min/ave:%.2f/%.2f/%.2f'%(runtime,tm.max(),tm.min(),tm.mean())
	else:
		return 'timecost should be list'

class download:

	def __init__(self,user='yyttrr3242342@163.com',passwd=None):
		if user is not None:
			if passwd is None:
				import mytools #used to get passwd from personal mysql
				passwd=mytools.getPasswd('renren',user)
			renrenId,detail=self.login(user,passwd)
			if renrenId is None:
				print('login failed,user={},{}'.format(user,detail))

	def friendList(self,renrenId='285060168',uppage=100):
		"""friendList('285060168') --> 
		return ({friend_rid1:name1,friend_rid2:name2},timecost) of renrenId,
		return (None,info) if error occurs, such as timeout or safetyPage"""
		return self.download_hdlr('friendList',renrenId,uppage)
	def status(self,renrenId='285060168',uppage=100):
		"""status('285060168') --> 
		(statusId,cur_content,orig_content,timestamp)"""
		return self.download_hdlr('status',renrenId,uppage)

	def profile(self,renrenId):
		"""profile('234234') -->
		return {tag1:value1,...,tagn:valuen} in detail page if available
		return {tag1:value1,...,tagn:valuen} in homepage if detail page unavailable
		return None if timeout"""
		pageStyle='profile_detail'
		html_content=self._one_page(urls[pageStyle].format(renrenId))
		if html_content is None:
			return None,'profile'
		elif html_content[0:30].find('<div class="col-left">') > -1:
			return parse.profile_detail(itemReg[pageStyle].findall(html_content)),'pf_detail'
		elif html_content[0:30].find('<!doctype html><html>') > -1:#tl
			#TODO:check whether account safety
			return parse.homepage_tl(itemReg['profile_tl'].findall(html_content)),'mini_tl'
		else:
			return parse.homepage_basic_privacy(itemReg['profile_basic'].findall(html_content)),'mini_basic'

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
			return None,'timeout'
		else:
			#check whether login is successful. 
			m=re.compile(r'http://www.renren.com/(\d+)').match(url)
			if m is None:
				return None,'login failed,rsp={}'.format(url)
			else:
				return m.group(1),'success'

	def download_hdlr(self,pageStyle,renrenId='285060168',uppage=100):
		"""pageStyle download handler.
		call _iter_page to request pages and detect items,
		parse record from items by parse module.runtime is logged."""
		runtime_start=time.time()
		req_time=[]
		items=self._iter_page(pageStyle,renrenId,range(0,uppage),req_time)
		meth_parse=getattr(parse,pageStyle)
		record=meth_parse(items)
		runtime=time.time()-runtime_start
		return record,format_time(runtime,req_time)

	def _one_page(self,url,request_time=None):
		"""onePage(url) --> 
		return html_content if success
		return None if timeout."""
		request_start=time.time()
		try:
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
	def _iter_page(self,pageStyle,renrenId,toDo=range(0,100),req_time=None):
		"""iterPage(pageStyle,renrenId)  --> 
		return itemsAll if success,return None if timeout after resend 3 times.
		raise exception if error or meet safety page"""
		itemsAll=set()
		timeout_seq=list()
		#request pages until no more items detected
		for curpage in toDo:
			html_content=self._one_page(urls[pageStyle].format(curpage,renrenId),req_time)
			if html_content is None:#add to timeout_seq to resend later.
				timeout_seq.append(curpage)
			else:
				items_curpage=itemReg[pageStyle].findall(html_content)#detect items
				if len(items_curpage) > 0:
					itemsAll |=  set(items_curpage)
				else:#privacy/all pages requested/safety page
					break
		#TODO:
		#resend if timeout_seq is not None and resend>0
		#self._iter_page(pageStyle,renrenId,timeout_seq,req_time,resend-1)
		#_empty_check if empty
		return itemsAll


	#@depraced
	def homepage(self,renrenId):
		pageStyle='homepage'
		html_content=self._one_page(urls[pageStyle].format(renrenId))
		if html_content is None:
			return set()
		elif html_content[0:30].find('<!doctype html><html>') > -1:#tl
			return parse.homepage_tl(itemReg[pageStyle+'_tl'].findall(html_content))
		else:
			return parse.homepage_basic(itemReg[pageStyle+'_basic'].findall(html_content))
	#@depraced
	def _emtpy_check(self,html_content):
		pageStyle='safety'
		m=itemReg[pageStyle].search(html_content)
		if m is None:
			return True,'not forbidden'
		else:
			return False,pageStyle

