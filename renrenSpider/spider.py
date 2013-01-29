from download import download
from db import rDb

user='jiekunyang@gmail.com'
dl=download(user)
db=rDb('ttt')

fl_searched=db.getSearched('relation')

def getNet2(rid='410941086'):
	fl=dl.friendList(rid)
	dl.out_timecost()
	db.insertFriendList(rid,fl)

	toSearch=set(fl.keys())-fl_searched
	for i,item in zip(range(len(toSearch)),toSearch):
		print('{}/{} searching,rid={},name={}'.format(i,len(toSearch),item,fl[item]))
		db.insertFriendList(item,dl.friendList(item))
		dl.out_timecost()
	dl.out_err()
#dl.out_timecost()

if __name__ == '__main__':
	rid=input('renrenId= ')
	getNet2(rid)
