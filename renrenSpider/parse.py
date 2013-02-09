_href_pf_prog=None
def friendList(href_pfs):
	"""friendList({'<a href="..?id=1">name1</a>','<a href="..?id=3">name2</a>'}) 
	--> return {id1:name1,id2:name2} if success,return None if error"""
	if href_pfs is None:
		return None
	elif isinstance(href_pfs,str):
		href_pfs={href_pfs}
	global _href_pf_prog
	if _href_pf_prog is None:
		import re
		_href_pf_prog=re.compile(r'id=(\d+)">([^<]*?)</a>')

	name=dict()
	for href_pf in href_pfs:
		m=_href_pf_prog.search(href_pf)
		if m is None:
			return None
		name[m.group(1)]=m.group(2)
	return name

_statprog=None
def status(stats):
	"""return {statusId:dict_of_details,statusId2:dict2} if success, return None if error"""
	if stats is None:
		return None
	elif isinstance(stats,str):
		stats={stats}
	global _statprog
	if _statprog is None:
		import re
		_statprog=re.compile(r'<li[^>]+id="status-(?P<id>\d+)">.+?<h3>\s*(?P<content>.+?)</h3>\s*?(?:<div class="content">\s*<div[^>]+>(?P<orig>.*?)</div>\s*</div>)?\s*<div class="details">.+?<span class="duration">(?P<timestamp>[^<]+?)</span>',re.DOTALL)

	res=dict()
	for stat in stats:
		m=_statprog.search(stat)
		if m is None:
			print('status parse error.stat={}'.format(stat))
			continue
		else:
			tmpStat=dict()
			status_id=m.group('id')
			tmpStat['renrenId1'],tmpStat['cur_name'],tmpStat['cur_content']=split_owner(drop_url(m.group('content')))
			tmpStat['orig_owner'],tmpStat['orig_name'],tmpStat['orig_content']=split_owner(drop_url(m.group('orig')))
			tmpStat['timestamp']=m.group('timestamp').strip()
			res[status_id]=tmpStat
	return res 

_profileprog=None
_profilegprog=None
def profile_detail(content):
	"""profile_detail({'<dt>name</dt><dd>zh</dd><dt>gender</dt>\n<dd>f</dd>',
	'<dt>birth</dt><dd>1993</dd><dt>city</dt>\n<dd>x</dd>'})
	-->{name:zh,gender:f,birth:1993,city:x}"""
	if content is None:
		return None
	global _profileprog
	global _profilegprog
	if _profileprog is None:
		import re
		_profileprog =re.compile(r'<dt>[^<]*?</dt>[^<]*?<dd>.*?</dd>',re.DOTALL)
		_profilegprog=re.compile(r'<dt>(.*?)</dt>[^<]*?<dd>(.*?)</dd>',re.DOTALL)

	content=drop_extra(str(content))
	items=_profileprog.findall(content)
	pf=dict()
	for item in items:
		pair=_profilegprog.search(item)
		value=pair.group(2).strip(' ')
		tag=pair.group(1).strip(' :：')
		pf[tag]=value
	return pf

_homepage_tlprog=None
_homepage_tlgprog=None
def homepage_tl(content):
	if content is None:
		return None
	global _homepage_tlprog
	global _homepage_tlgprog
	if _homepage_tlprog is None:
		import re
		_homepage_tlprog=re.compile(r'<li[^>]+?>.*?</li>',re.DOTALL)
		_homepage_tlgprog=re.compile(r'<li\sclass="(\w+?)">(.*?)</li>',re.DOTALL)

	content=drop_extra(str(content))
	items=_homepage_tlprog.findall(content)
	mini_pf=dict()
	for item in items:
		pair=_homepage_tlgprog.search(item)
		tag=pair.group(1)
		value=pair.group(2).strip(' ')
		if tag == 'birthday':
			mini_pf['gender'],mini_pf['birth']=split_tlbirth(value)
		else:
			mini_pf[tag]=value
	if None in mini_pf.values():
		return None
	else:
		return mini_pf

_homepage_basicprog=None
_homepage_basicgprog=None
def homepage_basic_privacy(content):
	if content is None:
		return None
	global _homepage_basicprog
	global _homepage_basicgprog
	if _homepage_basicprog is None:
		import re
		_homepage_basicprog=re.compile(r'<li[^>]+?>.*?</li>',re.DOTALL)
		_homepage_basicgprog=re.compile(r'<li\sclass="(\w+?)">(.*?)</li>',re.DOTALL)

	content=drop_extra(str(content))
	items=_homepage_basicprog.findall(content)
	mini_pf=dict()
	for item in items:
		pair=_homepage_basicgprog.search(item)
		if pair is None:
			print(item)
		else:
			mini_pf[pair.group(1)]=pair.group(2).strip(' ')
	return mini_pf

def split_tlbirth(value):
	if value is None:
		return None
	"""split_tlbirth(gender, birth) --> (gender,birth)"""
	#span/href/space is dropped before split
	tmp=value.replace('，',',').split(',')
	if len(tmp) < 2:
		return None,'src={},res={}'.format(value,tmp)
	else:
		return tmp[0].strip(' '),tmp[1].strip(' ')

_linkprog=None
def drop_href(content):
	if content is None:
		return None
	global _linkprog
	if _linkprog is None:
		import re
		_linkprog=re.compile(r'<a\s[^>]+?>([^<]*?)</a>')
	return _linkprog.sub(r'\1',content)

_spanprog=None
def drop_span(content):
	if content is None:
		return None
	global _spanprog
	if _spanprog is None:
		import re
		_spanprog=re.compile(r'<span(?:\sclass="link")*?>([^<]*?)</span>')
	return _spanprog.sub(r'\1',content)

_spaceprog=None
def drop_space(content):
	if content is None:
		return None
	global _spaceprog
	if _spaceprog is None:
		import re
		_spaceprog=re.compile(r'(?:&nbsp;)|(?:\\n)|\n|(?:\\u3000)|(?:\u3000)|(?:\\t)|\t')
	return _spaceprog.sub(r'',str(content)).strip(' ')

_multispaceprog=None
def combine_space(content):
	if content is None:
		return None
	global _multispaceprog
	if _multispaceprog is None:
		import re
		_multispaceprog=re.compile(r'\s+')
	return _multispaceprog.sub(r' ',content).strip('')

def drop_extra(content):
	return drop_space(drop_span((drop_href(content))))

_pfprog=None
def drop_pf(content):
	if content is None:
		return None
	global _pfprog
	if _pfprog is None:
		import re
		_pfprog=re.compile(r'<a\W[^>]+?http://www.renren.com/profile.do\?id=(\d+)[^>]+>(.*?)</a>',re.DOTALL)
	return _pfprog.sub(r'(\1,\2)',content)

_pubpfprog=None
def drop_pubpf(content):
	if content is None:
		return None
	global _pubpfprog
	if _pubpfprog is None:
		import re
		_pubpfprog=re.compile(r'<a\W[^>]+?http://page.renren.com/(\d+)[^>]+>(.*?)</a>',re.DOTALL)
	return _pubpfprog.sub(r'(\1,\2)',str(content))

_atprog=None
def drop_at(content):
	if content is None:
		return None,None
	global _atprog
	if _atprog is None:
		import re
		_atprog=re.compile(r"<a\W[^>]+?http://www.renren.com/g/(\d+)[^>]*>(@.*?)</a>",re.DOTALL)
	return _atprog.sub(r'\2(\1)',str(content))

_imgprog=None
def drop_img(content):
	if content is None:
		return None
	global _imgprog
	if _imgprog is None:
		import re
		_imgprog=re.compile(r"<img\W[^>]+alt=\'([^>]*?)\'[^>]*?/>",re.DOTALL)
	return _imgprog.sub(r'(img\1img)',content)

def drop_url(content):
	if content is None:
		return None
	else:
		return combine_space(drop_rrurl(drop_img(drop_pf(drop_pubpf(drop_at(content))))))

_rrurlprog=None
def drop_rrurl(content):
	if content is None:
		return None
	global _rrurlprog
	if _rrurlprog is None:
		import re
		_rrurlprog=re.compile(r"<a\W[^>]+title='([^>]+)'>[^<]+</a>",re.DOTALL)
	return _rrurlprog.sub(r'(\1)',content)

def split_owner(content):
	if content is None:
		return None,None,None
	else:
		idx=content.replace('：',':').find(':')
		idx2=content.find(',')
		if (idx < 0) or (idx2 <0):
			return None,None,None
		return content[:idx2].strip('( '),content[idx2+1:idx].strip(') '),content[idx+1:].strip(' ')
