# -*- coding: utf-8-*-
import sys
import spider

cfg_filename='config/spider.ini'

config=None
def get_cfg_dict(section_name,has_default=True):
	global config
	if config is None:
		import configparser
		config=configparser.ConfigParser()
	# global cfg_filename
	config.read(cfg_filename)
	try:
		cfg=dict(config[section_name].items())
	except KeyError:
		# raise error, no such section
		return None
	if not has_default:
		for key in config['DEFAULT'].keys():
			del(cfg[key])
	return cfg

def init_config():
	config_account=get_cfg_dict('account')
	config_repo=get_cfg_dict('repo')

	repo_name=config_repo['repo_name_pre']   # table name prefix
	repo_mode=config_repo['mode']   # table name prefix
	user=config_account['user']  # renren account
	passwd=config_account['passwd']  # renren passwd
	# adopt for myself
	if passwd ==  'None':
		passwd=None
	print('config inited')
	return repo_mode,repo_name,user,passwd

def run(meth,orig_id=None):
	repo_mode,repo_name,user,passwd=init_config()
	spider.set_repo(repo_mode)
	tt=spider.spider(repo_name,user,passwd)
	tt.log.setLevel(20)
	my_rid,login_info=tt.login()
	if my_rid is None:
		print('spider login error. detail:{}'.format(login_info))
		if not input('continue for test?(1/0)'):
			return None
		else:
			my_rid='11111111'
	else:
		print('spider login success. rid={}'.format(my_rid))
	if orig_id is None:
		orig_id = my_rid
	meth(tt,orig_id)

def pub_meth(obj):
	meths=set()
	for meth in dir(obj):
		if meth.startswith('get'):
			meths.add(meth)
	return meths

if __name__ == '__main__':
	try:
		meth=getattr(spider.spider,sys.argv[1])
	except AttributeError:
		print('method {} not definded. method list: {}'.format(sys.argv[1],pub_meth(spider.spider)))
	except IndexError:
		print('input error, method is necessary. expect: python3 get_info method renrenId.')
	else:
		if len(sys.argv) == 2:
			orig_id=None
		elif len(sys.argv) == 3:
			orig_id=sys.argv[2]
		else:
			print('input error. expect: method, renrenId')
		run(meth,orig_id)
