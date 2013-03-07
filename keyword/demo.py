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

kword=dict()
for timestamp,status in getStatus('233330059').items():
	for word in jieba.cut(status,cut_all=False):
		try:
			# timestamp to be set() to avoid repeat word in the same status
			kword[word]=kword.get(word,set())
			kword[word].add(timestamp)
		except AttributeError:
			print(u'{},{}'.format(timestamp,word))

freq=[]
for k,v in kword.items():
	freq.append((len(v),k))

freq.sort()

for k,v in freq:
	print(u'{},{}'.format(k,v))
#print(len(kword))
