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
		_ignore={
			u'我',u'你',  # pron
			u'和',u'的',u'了',u'又'}
	for k in _ignore:
		data.pop(k)
	return data

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
	return kword


rid='233330059'
status=getStatus(rid)
kword=extract_keyword(status)
kword=drop_ignore(kword)

# drop all single-character word, except words in keep_set
single=[]
for k in kword.keys():
	if len(k) < 2:
		single.append(k)
print("',u'".join(single))

freq=[]
for k,v in kword.items():
	freq.append((len(v),k))

freq.sort()

for k,v in freq:
	pass
	#print(u'{},{}'.format(k,v))
print(len(kword))
