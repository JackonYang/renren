import unittest
from test_browser import *
from test_file import *
from test_mysql import *
from test_parse import *

if __name__=='__main__':
	suite=unittest.TestSuite()

	# browser
	# the two below only test when great changes have taken place
	# and all other testcase passed, because Internet is needed and login()
	#suite.addTest(test_browser('test_login'))#login
	#suite.addTest(test_browser('test_download'))#login and download
	suite.addTest(test_browser('test_friendList'))
	suite.addTest(test_browser('test_status'))
	suite.addTest(test_browser('test_profile'))
	# testcase to check test_tools
	suite.addTest(test_browser('test_new_browser'))
	# private method of browser
	suite.addTest(test_browser('test_iter_page'))
	suite.addTest(test_browser('test_iter_page_timeout'))

	# repo_file
	suite.addTest(test_repo_file('test_save_status'))
	suite.addTest(test_repo_file('test_save_friendList'))
	suite.addTest(test_repo_file('test_getSearched'))
	suite.addTest(test_repo_file('test_getFriendList'))

	# repo_mysql
	suite.addTest(test_repo_mysql('test_save_status'))
	suite.addTest(test_repo_mysql('test_save_friendList'))
	suite.addTest(test_repo_mysql('test_save_profile'))
	suite.addTest(test_repo_mysql('test_getSearched'))
	suite.addTest(test_repo_mysql('test_getFriendList'))
	# private method of repo_mysql
	suite.addTest(test_repo_mysql('test_save_history'))
	suite.addTest(test_repo_mysql('test_tableManage'))
	suite.addTest(test_repo_mysql('test_read_cfg'))

	# parse
	suite.addTest(test_parse('test_friendList'))  # full test
	suite.addTest(test_parse('test_profile_detail'))  # full test
	suite.addTest(test_parse('test_profile_mini'))  # full test
	# private method of parse
	#suite.addTest(test_parse('test_get_birth'))#full test
	#suite.addTest(test_parse('test_get_gender'))#full test
	#suite.addTest(test_parse('test_split_high_edu'))#full test
	#suite.addTest(test_parse('test_split_low_edu'))#full test
	suite.addTest(test_parse('test_sub_space'))  # full test
	#suite.addTest(test_parse('test_drop_link'))
	#suite.addTest(test_parse('test_drop_pf_extra'))
	#suite.addTest(test_parse('test_drop_href'))
	#suite.addTest(test_parse('test_drop_span'))
	#suite.addTest(test_parse('test_drop_rrurl'))
	#suite.addTest(test_parse('test_split_owner'))

	runner=unittest.TextTestRunner()
	runner.run(suite)
