import download
import time

user='jiekunyang@gmail.com'
dl=download.download(user)

fl_searched=set()#db.getSearched('relation')

def getNet2(rid='410941086'):
	fl,timecost=dl.friendList(rid)
	#db.insertFriendList(rid,fl)
	toSearch=set(fl.keys())-fl_searched
	print('renrenId={},toSearch/total:{}/{}'.format(rid,len(toSearch),len(fl)))
	for i,item in zip(range(len(toSearch)),toSearch):
		friends,timecost=dl.friendList(item)
		print('{}/{} {},{},{},{} friends,{}'.format(i,len(toSearch),time.strftime('%H:%M:%S',time.localtime()),item,fl[item],len(friends),timecost))
		#db.insertFriendList(item,friends)

if __name__ == '__main__':
	rid=input('renrenId= ')
	getNet2(rid)
