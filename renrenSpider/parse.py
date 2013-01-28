details={
	#basic
	'生日':'birth','星座':'star','家乡':'hometown','性别':'gender',
	#edu
	'大学':'edu_college','高中':'edu_senior','中专技校':'edu_tech','初中':'edu_junior','小学':'edu_primary',
	#work
	'公司':'company','时间':'work_time',
	#contact
	'QQ':'qq','MSN':'msn','手机号':'phone','个人网站':'personal_website','我的域名':'domain1','个性域名':'domain2',
	#mini_pf
	'所在城市':'address','所在公司':'work','所在学校':'school','等级':'rrlvl','生肖':'shengxiao'
	}

_nameprog=None
def friendList(pfHrefs):
	"""friendList({'<a href="..?id=1">name1</a>','<a href="..?id=3">name2</a>'}) 
	--> {id1:name1,id2:name2}"""
	global _nameprog
	if _nameprog is None:
		import re
		_nameprog=re.compile(r'id=(\d+)">([^<]*?)</a>')

	if isinstance(pfHrefs,str):
		pfHrefs={pfHrefs}
	name=dict()
	for pfHref in pfHrefs:
		m=_nameprog.search(pfHref)
		if m is None:
			return None
		name[m.group(1)]=m.group(2)
	return name

_profileprog=None
_profilegprog=None
def profile_detail(content):
	"""profile_detail({'<dt>name</dt><dd>zh</dd><dt>gender</dt>\n<dd>f</dd>',
	'<dt>birth</dt><dd>1993</dd><dt>city</dt>\n<dd>x</dd>'})
	-->{name:zh,gender:f,birth:1993,city:x}"""
	global _profileprog
	global _profilegprog
	if _profileprog is None:
		import re
		_profileprog =re.compile(r'<dt>[^<]*?</dt>[^<]*?<dd>.*?</dd>',re.DOTALL)
		_profilegprog=re.compile(r'<dt>(.*?)</dt>[^<]*?<dd>(.*?)</dd>',re.DOTALL)

	items=_profileprog.findall(str(content))
	pf=dict()
	for item in items:
		pair=_profilegprog.search(item)
		value=drop_extra(pair.group(2))
		if value=='':
			continue
		else:
			tag=details[drop_extra(pair.group(1))]
			pf[tag]=value
	return pf

_homepage_tlprog=None
_homepage_tlgprog=None
def homepage_tl(content):
	global _homepage_tlprog
	global _homepage_tlgprog
	if _homepage_tlprog is None:
		import re
		_homepage_tlprog=re.compile(r'<li[^>]+?>.*?</li>',re.DOTALL)
		_homepage_tlgprog=re.compile(r'<li\sclass="(\w+?)">(.*?)</li>',re.DOTALL)

	items=_homepage_tlprog.findall(str(content))
	mini_pf=dict()
	for item in items:
		pair=_homepage_tlgprog.search(item)
		tag=pair.group(1)
		value=drop_extra(pair.group(2))
		if tag == 'birthday':
			mini_pf['gender'],mini_pf['birth']=tlbirth(value)
		elif tag == 'school':
			mini_pf['school']=cut_tlpf_school(value)
		else:#address and hometown, drop head.
			mini_pf[tag]=value[2:]
	return mini_pf 

def homepage_basic(content):
	content=str(content)
	if content[:5].find('ul')>0:
		return homepage_basic_privacy(content)
	else:
		return profile_detail(content)


_homepage_basicprog=None
_homepage_basicgprog=None
_spanprog=None
def homepage_basic_privacy(content):
	global _homepage_basicprog
	global _homepage_basicgprog
	global _spanprog
	if _homepage_basicprog is None:
		import re
		_homepage_basicprog=re.compile(r'<li[^>]+?>.*?</li>',re.DOTALL)
		_homepage_basicgprog=re.compile(r'<li\sclass="(\w+?)">\w+<span[^>]+>(.*?)</span>\w*?</li>',re.DOTALL)
		_spanprog=re.compile(r'</span><spanclass="link">')

	items=_homepage_basicprog.findall(content)
	mini_pf=dict()
	for item in items:
		pair=_homepage_basicgprog.search(item)
		tag=drop_extra(pair.group(1))
		value=drop_extra(pair.group(2))
		if tag == 'hometown':
			value=_spanprog.sub('',value)
		mini_pf[tag]=value
	return mini_pf

_tlpf_birthprog=None
def tlbirth(content):
	global _tlpf_birthprog
	if _tlpf_birthprog is None:
		import re
		_tlpf_birthprog=re.compile(r'<span>(\w+)</span><span>\D*(\w+)</span>')
	m=_tlpf_birthprog.search(content)
	return m.group(1,2)

_tlpf_spanprog=None
def cut_tlpf_school(content):
	global _tlpf_spanprog
	if _tlpf_spanprog is None:
		import re
		_tlpf_spanprog=re.compile(r'<span>就读于(\w+)</span>')
	m=_tlpf_spanprog.search(content)
	if m is None:
		return content
	else:
		return m.group(1)

_linkprog=None
def drop_href(content):
	global _linkprog
	if _linkprog is None:
		import re
		_linkprog=re.compile(r'<a\s[^>]+?>([^<]*?)</a>')
	return _linkprog.sub(r'\1',content)
	
_extraprog=None
def drop_extra(content):
	global _extraprog
	if _extraprog is None:
		import re
		_extraprog=re.compile(r'(?:&nbsp;)|(?:\"\+response\.[a-z]+\+\")|\s+|(?:\\n)|(?:\\u3000)|(?:\\t)|:')
	return _extraprog.sub(r'',drop_href(content))

