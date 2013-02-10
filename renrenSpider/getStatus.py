import spider

user='jiekunyang@gmail.com'
db='renren_orig'
#target='233330059'
#target='410941086'
target='230760442'
tt=spider.spider(user,db)
tt.getStatus_friend(target)
