#encoding=utf-8
import pymysql
import jieba

def getStatus(rid,table_pre='orig_renren'):
	tablename='{}_{}'.format(table_pre,'status')
	conn=pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='Kunth123', db='data_bang',charset='utf8')
	cur=conn.cursor()
	cur.execute("select timestamp,cur_content from {} where renrenId1='{}'".format(tablename,rid))
	res={}
	for content in cur.fetchall():
		res[content[0]]=content[1]
	cur.close()
	conn.close()
	return res

_ignore=None
def drop_ignore(data):
	global _ignore
	if _ignore is None:
		_ignore={u'要',u'的',u'了',u'有',u'很',u'上',u'不',u'和',u'我',u'给',u'一个',u'在',u'被',u'是',u'就',u'到',u'现在',u'人',u'今天',u'又',u'啊',u'自己',u'这',u'还',u'去',u'也',u'你',u'好',u'可以',u'让',u'说',u'都',u'就是',u'转自',u'img',
			# 2000 up
			u'谁',u'一',u'吃',u'这么',u'一下',u'什么',u'把',u'再',u'小',u'得',u'大',u'如果',u'手机',u'多',u'我们',u'没',u'那',u'会',u'生活',u'还是',u'大笑',u'没有',u'个',u'明天',u'事',u'知道',u'着',u'过',u'等',u'不是',u'才',u'里',u'真的',u'这个',u'终于',u'比',u'他',u'怎么',u'呢',u'来',u'这是',u'大家',u'看',u'吧',u'下',u'走',u'想',u'中',u'请',u'对',u'已经',u'能',u'同学',u'看到',u'这样',
			# more
			u'做',u'跟',u'用',u'从',u'找',u'月',u'但是',u'开始',u'然后',u'突然',u'以后',u'还有',u'貌似',u'不用',u'应该',u'感觉',u'发现',u'需要',u'刚刚',
			# time
			u'早晨',u'中午',u'上午',u'下午',u'晚上',u'今天',u'今天下午',u'今天上午'
			}
	for k in _ignore & set(data.keys()):
		data.pop(k)

def _fix_little_age(kword):
	if (u'小时' in kword) and (u'时候' in kword):
		nxs=kword[u'小时']
		nsh=kword[u'时候']
		if nxs < nsh:
			kword.pop(u'小时')
			kword[u'小时候']=nxs
			kword[u'时候']=nsh-nxs
		elif nsh < nxs:
			kword.pop(u'时候')
			kword[u'小时候']=nsh
			kword[u'小时']=nxs-nsh
		else:
			kword.pop(u'时候')
			kword.pop(u'小时')
			kword[u'小时候']=nsh

# extract keyword
def extract_keyword(status):
	kword=dict()
	for timestamp,status in status.items():
		for word in jieba.cut(status,cut_all=False):
			# timestamp to be set() to avoid repeat word in the same status
			if word in kword:
				kword[word].add(timestamp)
			else:
				kword[word]={timestamp}
	_fix_little_age(kword)
	drop_ignore(kword)
	return kword

def show_all_keyword(friend):
	rid='233330059'
	res=extract_keyword(getStatus(rid))
	for rid in friend:
		kword=extract_keyword(getStatus(rid))
		res.update(kword)
		print(len(res))
	sort_freq(res)

def get_common_keyword(friend):
	# init res by someone whose keyword more than bound
	rid='233330059'
	res=set(extract_keyword(getStatus(rid)).keys())
	did=0
	undo=0
	for i,rid in zip(range(1,len(friend)+1),friend):
		kword=extract_keyword(getStatus(rid))
		if len(kword)>2000:
			did += 1
			res &= set(kword.keys())
		else:
			undo += 1
			print(u'{} number of keyword < 2000 {} {}'.format(undo,friend[rid],len(kword)))
	print(u"common keyword to add to ignore list: {}".format("',u'".join(res)))
	print(len(friend),did,undo)

def _drop_single_word(kword):
	for k in kword.keys():
		if len(k) < 2:
			kword.pop(k)

def sort_freq(kword):
	# fix
	_drop_single_word(kword)
	freq=[]
	for k,v in kword.items():
		if len(v) > 1:
			freq.append((len(v),k))
	freq.sort()
	for k,v in freq:
		print(u'{},{}'.format(k,v))

def show_kword(rid):
	status=getStatus(rid)
	kword=extract_keyword(status)
	sort_freq(kword)

def nstatus_nkeyword(friend):
	data=[]
	for i,rid in zip(range(1,len(friend)+1),friend):
		status=getStatus(rid)
		kword=extract_keyword(status)
		data.append((len(status),len(kword)))
	return data

plt=None
def plot_tuple(data):
	global plt
	if plt is None:
		import matplotlib.pyplot as plt
	data.sort()
	x=[]
	y=[]
	for a,b in data:
		x.append(a)
		y.append(b)
	fig=plt.figure()
	plt.plot(x,y,'o')
	plt.grid(True)
	plt.show()

if __name__ == '__main__':
	import mytools
	friend=mytools.getFriend()
	#get_common_keyword(friend)
	#show_all_keyword(friend)
	# data=nstatus_nkeyword(friend)
	# plot_tuple(data)
	rid='233330059'
	#rid = '232279547'
	show_kword(rid)

