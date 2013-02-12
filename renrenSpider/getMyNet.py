import spider

user='jiekunyang@gmail.com'
repo_name='my_net'

tt=spider.spider(user,repo_name)
my_rid,login_info=tt.login()
if my_rid is None:
	print('spider login error.detail:{}'.format(login_info))
else:
	print('spider login success.rid={}'.format(my_rid))
	tt.getNet2(my_rid)
