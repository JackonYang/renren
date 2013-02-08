import testBrowser

#friendList={'240303471':0,'446766202':1,'500275848':2,'444024948':20,'384065413':21,'397529849':22,'739807017':40}
#status={'446766202':0,'500275848':1,'104062077':2,'232877604':20,'242641331':21,'256137627':22,'411984911':40}
friendList=dict()#{'287286312':110}
status={'259364921':110}

dl=testBrowser.new_browser()

for rid in friendList.keys():
	dl.get_test_data('friendList',rid)
for rid in status.keys():
	dl.get_test_data('status',rid)
