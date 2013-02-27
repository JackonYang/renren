import spider
import mytools

repo_name='orig_renren' #table name prefix
user='jiekunyang@gmail.com' #renren account
passwd=None #renren passwd

tt=spider.spider(repo_name,user,passwd)
#tt.log.setLevel(40)
my_rid,login_info=tt.login()
if my_rid is None:
	print('spider login error.detail:{}'.format(login_info))
else:
	print('spider login success.rid={}'.format(my_rid))

	#start to search
	friends=mytools.getFriend()
	for rid in friends.keys():
		tt.getProfile_friend(rid)
