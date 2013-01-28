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
details={
	'等级':'rrlvl',
	#basic
	'生日':'birth','星座':'star','家乡':'hometown','性别':'gender',
	#edu
	'大学':'edu_college','高中':'edu_senior','中专技校':'edu_tech','初中':'edu_junior','小学':'edu_primary',
	#work
	'公司':'company','时间':'work_time',
	#contact
	'QQ':'qq','MSN':'msn','手机号':'phone','个人网站':'personal_website','我的域名':'domain1','个性域名':'domain2'}
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
		value=drop_extra(drop_href(pair.group(2)))
		if value=='':
			continue
		else:
			tag=details[drop_extra(pair.group(1))]
			pf[tag]=value
	return pf

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
		_extraprog=re.compile(r'(?:&nbsp;)|(?:\"\+response\.[a-z]+\+\")|\s+|(?:\\n)|(?:\\t)|:')
	return _extraprog.sub(r'',content)

