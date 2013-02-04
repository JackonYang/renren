_nameprog=None
def friendList(pfHrefs):
	"""friendList({'<a href="..?id=1">name1</a>','<a href="..?id=3">name2</a>'}) 
	--> 
	return {id1:name1,id2:name2} if success
	return dict() if pfHrefs is set()
	return None if no group searched in one element of pfHrefs
	return None if pfHrefs is None
	"""
	if pfHrefs is None:
		return None
	elif isinstance(pfHrefs,str):
		pfHrefs={pfHrefs}
	global _nameprog
	if _nameprog is None:
		import re
		_nameprog=re.compile(r'id=(\d+)">([^<]*?)</a>')

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
		_spaceprog=re.compile(r'(?:&nbsp;)|(?:\"\+response\.[a-z]+\+\")|(?:\\n)|\n|\t|(?:\\u3000)|(?:\\t)')
	return _spaceprog.sub(r'',str(content)).strip(' ')

def drop_extra(content):
	return drop_space(drop_span((drop_href(content))))

