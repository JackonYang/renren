import test_browser

status=dict()
friendList=dict()
#friendList={'240303471':0,'446766202':1,'500275848':2,'444024948':20,'384065413':21,'397529849':22,'739807017':40,'287286312':110}
#status={'446766202':0,'500275848':1,'104062077':2,'232877604':20,'242641331':21,'256137627':22,'411984911':40,'259364921':110}
#profile={'233330059','294126602','223981104','240303471','222420915','285060168'}
profile={'271600917'}

#friendList={'119815062':170}
dl=test_browser.new_browser()
for rid in friendList.keys():
	dl.get_test_data('friendList',rid)
for rid in status.keys():
	dl.get_test_data('status',rid)
for rid in profile:
	dl.get_test_data('profile',rid)
