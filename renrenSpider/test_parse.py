import unittest
import parse
from browser import browser

class Test_parse(unittest.TestCase):

	def setUp(self):
		pass
	def tearDown(self):
		pass

	def test_friendList(self):
		pfHrefs=[
			{'<dd><a href="http://www.renren.com/profile.do?id=6754031">王瑛</a>',
			'<dd><a href="http://www.renren.com/profile.do?id=331442">En.王哲</a>'},
			{'<dd><a href="http://www.renren.com/profile.do?id=9439171"></a>'},
			'<dd><a href="http://www.renren.com/profile.do?id=34134">～@%……</a>',
			{},
			{'error'},
			None
			]
		names=[
			{'6754031':'王瑛','331442':'En.王哲'},
			{'9439171':''},
			{'34134':'～@%……'},
			{},
			None,
			None]
		for pfHref,name in zip(pfHrefs,names):
			self.assertEquals(parse.friendList(pfHref),name)

	def test_profile_detail(self):
		contents={
			#some items with no space
			"""<dt>性别:</dt><dd>女</dd>,\
			<dt>大学:</dt><dd><a st>北学</a>-<a st>2013年</a>-<a st>学院</a><br><a st>理工大学</a>-<a st>2011年</a>-<a st>生命学院</a><br></dd>,\
			<dt>小学:</dt><dd><a st>一个小学</a>-<a st>1991年</a><a st>青岛二小</a>-<a st>2001年</a></dd>"""
			:{'性别': '女',
				'大学': '北学-2013年-学院<br>理工大学-2011年-生命学院<br>',
				'小学': '一个小学-1991年青岛二小-2001年'},
			#some items with space and \n \t
			"""<dt> 性别 : </dt> <dd> 女 </dd> , \
			<dt> 大学 : </dt>\n\\n<dd>\n\\n<a st>\n\\n北京中医药大学\n</a> - <a st>\n 2013年\n </a> - <a st> 东方学院 </a><br>\
				<a st> 北京理工大学\t\t</a> - <a st> 2011年 </a> - <a st> 生命科学与技术学院六院 </a><br></dd>,\
			<dt> 小学 : </dt><dd><a st> 一个小学 </a> - <a st> 1991年 </a><a st> 青岛二小 </a> - <a st> 2001年 </a></dd>"""
			:{'性别': '女',
				'大学': '北京中医药大学 - 2013年 - 东方学院 <br> 北京理工大学 - 2011年 - 生命科学与技术学院六院 <br>',
				'小学': '一个小学 - 1991年 青岛二小 - 2001年'},
			#no items or None
			"""no item""":{},None:None}
		for  content,expt in contents.items():
			if content is not None:
				content=content.split(',')
				self.assertEquals(parse.profile_detail(content),expt)

	def test_profile_mini(self):
		contents={
			#full items with space
			"""<ul class="information-ul" id="information-ul" onclick href='http:'">\\n\n\t\\t\
			<li class="school"> \n\\n\t\\t<span>\n就读于西北大学\n</span>\t\\t</li>\n\t\
			<li class="birthday">\n\\n<span class="link">\t男生\n\\n</span>\\n\n<span> ，2月13日\\n</span>\t\\t</li> \
			<li class="hometown">\n\\n来自内蒙古\n\\n<a stats="info_info">\n延安市\n</a>\n\\n</li>\n\\n\
			<li class="address">\\n现居\\n山南地区 </li> </ul>"""
			:{'school':'就读于西北大学',
			'gender':'男生 ',
			'birthday':'2月13日',
			'hometown':'来自内蒙古 延安市',
			'address':'现居 山南地区'},
			#full items with no space
			"""<ul class="information-ul" id="information-ul" onclick href='http:'">\
			<li class="school"><span>就读于西北大学</span></li>
			<li class="birthday"><span class="link">男生</span><span>，2月13日</span></li>
			<li class="hometown">来自内蒙古<a stats="info_info">延安市</a></li>
			<li class="address">现居山南地区</li></ul>"""
			:{'hometown':'来自内蒙古延安市','school':'就读于西北大学','birthday':'2月13日','gender':'男生','address':'现居山南地区'},
			#full items with space. basic
				"""<ul class="user-info clearfix">\
				<li class="gender">\n\t\\t<span class="link">\\n男生\t</span></li>\t\\t\n\\n\
				<li class="hometown">\n\t\\n来自\\n<span>\\n\n山东\n\\t</span>\n\\n <a href="">烟台市\t\\t\n\\n</a></li>\
				<li class="school">\n\\n在\t\\t<span class="link">\t\\tFachhochschule Aachen\t\\t</span>\n\\t读书\\t</li></ul>"""
				:{'gender': '男生', 'school': '在 Fachhochschule Aachen 读书', 'hometown': '来自 山东 烟台市'},
				#full items without space
				"""<ul class="user-info clearfix"><li class="gender">\
				<span class="link">男生</span></li>\
				<li class="hometown">来自<span>山东</span><a href="">烟台市</a></li>\
				<li class="school">在<span class="link">Fachhochschule Aachen</span>读书</li></ul>"""
				:{'gender':'男生', 'school':'在Fachhochschule Aachen读书','hometown':'来自山东烟台市'},
				#no items or None
				"""<ul class="user-info clearfix"></ul>""":{},None:None}
		for content,expt in contents.items():
				self.assertEquals(parse.profile_mini(content),expt)

	#basic info
	def test_get_birth(self):
		contents={'80 后 10 月 12 日天秤座':{'birth_day': '12', 'birth_month': '10', 'birth_year': '80'},# xx后 and int(2)
				'2012年8月1日狮子座':{'birth_day': '1', 'birth_month': '8', 'birth_year': '2012'},# xx年 and int(1)
				' 3 月 6 日 双鱼座':{'birth_day': '6', 'birth_month': '3', 'birth_year': '9999'},#no age info
				'1987年9月1日':{'birth_day': '1', 'birth_month': '9', 'birth_year': '1987'},#no star info
				'3 月 29 日':{'birth_day': '29', 'birth_month': '3', 'birth_year': '9999'},#no age or star info
				'3-29':{'birth_day': '29', 'birth_month': '3', 'birth_year': '9999'},#no age or star info
				'3 - 31':{'birth_day': '31', 'birth_month': '3', 'birth_year': '9999'},#no age or star info
				'2011-9-1':{'birth_day': '1', 'birth_month': '9', 'birth_year': '2011'},#no star info
				'1993 - 9 - 1':{'birth_day': '1', 'birth_month': '9', 'birth_year': '1993'},#no star info
				'9999-99-99':{'birth_day':'99','birth_month':'99','birth_year':'9999'},
				'男,':{'birth_day':'99','birth_month':'99','birth_year':'9999'},
				'':{'birth_day':'99','birth_month':'99','birth_year':'9999'},
				None:{'birth_year':None,'birth_month':None,'birth_day':None}
				}
		for content,expt in contents.items():
			self.assertEquals(parse._get_birth(content),expt)
	def test_get_gender(self):
		contents={'他是男生':'m','男生':'m','她是女生':'f','女生':'f','女':'f','男':'m','no match':'u',None:None}
		for content,expt in contents.items():
			self.assertEquals(parse._get_gender(content),expt)

	#edu info
	def test_split_high_edu(self):
		contents={
				# two item, full space
				' Birmingam City - 2011 年 - 其它院系 <br> 西北大学 - 2012 年 - 其它院系 <br> '
				:[{'major': '其它院系', 'name': 'Birmingam City', 'year': '2011'}, {'major': '其它院系', 'name': '西北大学', 'year': '2012'}],
				# two item, no space
				'Birmingam City-2011年-其它院系<br>西北大学-2012年-其它院系<br>'
				:[{'major': '其它院系', 'name': 'Birmingam City', 'year': '2011'}, {'major': '其它院系', 'name': '西北大学', 'year': '2012'}],
				# one item, no space
				'西北大学-2010年-物理学系<br>':[{'major': '物理学系', 'name': '西北大学', 'year': '2010'}],
				# English with useful space. can't drop
				'Lincoln University - 1970年 <br>':[{'major': '', 'name': 'Lincoln University', 'year': '1970'}],
				'no match':[],
				None:None
				}
		for content,expt in contents.items():
			self.assertEquals(parse._split_high_edu(content),expt)
	def test_split_low_edu(self):
		contents={
				# full space
				' 万州上海中学 - 2009年 万州高级中学 - 2012年 '
				:[{'name': '万州上海中学', 'year': '2009'}, {'name': '万州高级中学', 'year': '2012'}],
				# no space
				'万州上海中学-2004年万州高级中学-2011年'
				:[{'name': '万州上海中学', 'year': '2004'}, {'name': '万州高级中学', 'year': '2011'}],
				#one item
				'三原县南郊中学- 2005年':
				[{'name': '三原县南郊中学', 'year': '2005'}],
				None:None
				}
		for content,expt in contents.items():
			#self.assertEquals(parse._split_low_edu(content),expt)
			print(parse._split_low_edu(content,'p'))

	#drops
	def test_sub_space(self):
		#replace space, and no effect on other word
		contents=['abcdefghijklmnopqrstuvwxyz0123456789 nntt003','\n\\n\t\\t &nbsp;\u3000\\u3000abcdefghijklmnopqrstuvwxyz0123456789&nbsp;\\n\n\\n\t\\u3000\u3000 nntt003']
		expt1='abcdefghijklmnopqrstuvwxyz0123456789 nntt003'
		expt2='abcdefghijklmnopqrstuvwxyz0123456789nntt003'
		for content in contents:
			self.assertEquals(parse._sub_space(content,r' '),expt1)
			self.assertEquals(parse._sub_space(content,r''),expt2)
	def test_drop_pf_extra(self):
		#replace space, and no effect on other word
		contents=['abcdefghijklmnopqrstuvwxyz0123456789 nntt003','\n\\n\t\\t \u3000\\u3000abcdefghijklmnopqrstuvwxyz0123456789\\n\n\\n\t\\u3000\u3000 nntt003']
		expt1='abcdefghijklmnopqrstuvwxyz0123456789 nntt003'
		expt2='abcdefghijklmnopqrstuvwxyz0123456789nntt003'
		for content in contents:
			self.assertEquals(parse._drop_pf_extra(content,r' '),expt1)
			self.assertEquals(parse._drop_pf_extra(content,r''),expt2)

	def test_drop_href(self):
		contents={"""<dt>生日\n\\n\t\\t :</dt><dd><a stats="info'> 1994\n\\n\t\\t </a> 年\n\\n\t\\t <a href="pf_star">摩羯座</a><a stats="info_info">陕西</a> \t\\t\n\\n """:"""<dt>生日\n\\n\t\\t :</dt><dd> 1994\n\\n\t\\t  年\n\\n\t\\t 摩羯座陕西 \t\\t\n\\n """,#all kinds of elements in and out <a></a>
		"""hello<dt>birth</dt>""":"""hello<dt>birth</dt>""",#no href
		"""<about>hello</about>""":"""<about>hello</about>""",#start with <a,but not href
		None:None
		}
		for content,expt in contents.items():
			self.assertEquals(parse._drop_link(content),expt)

	def test_drop_span(self):
		contents={"""\n\\n\t\\t<span>\n\\n\t\\t男生boy123\n\\n\t\\t</span> \n\\n\t\\t <span>，2月13日</span>""":"""\n\\n\t\\t\n\\n\t\\t男生boy123\n\\n\t\\t \n\\n\t\\t ，2月13日""",#span with all kinds of items
			"""\n\\n\t\\t<span class="link">\n\\n\t\\t男生boy123\n\\n\t\\t</span> \n\\n\t\\t <span class="link">，2月13日</span>""":"""\n\\n\t\\t\n\\n\t\\t男生boy123\n\\n\t\\t \n\\n\t\\t ，2月13日""",#spanclasslink with all kinds of items
			"""<span class="link">boy</span><span>男生</span>""":"""boy男生""",#multi
			"""nospan""":"""nospan""",
			None:None
		}
		for content,expt in contents.items():
			self.assertEquals(parse.drop_span(content),expt)

	def test_drop_rrurl(self):
		contents={"<a href='http://rrurl.cn/pN' target='_blank' title='http://lang-8.com/'>http://rrurl.cn/pNVUbN </a>":'(http://lang-8.com/)',
			None:None,
			'norrurl':'norrurl'
		}
		for content,expt in contents.items():
			self.assertEquals(parse.drop_rrurl(content),expt)

	def test_split_owner(self):
		contents={' (123456,name) : testcase':('123456','name','testcase'),None:(None,None,None),'no ptn':(None,None,None),'32:only':(None,None,None),'asdf,only':(None,None,None)}
		for content,expt in contents.items():
			self.assertEquals(parse.split_owner(content),expt)

if __name__=='__main__':
	suite=unittest.TestSuite()

	#checked
	suite.addTest(Test_parse('test_friendList'))#full test
	suite.addTest(Test_parse('test_profile_detail'))#full test
	suite.addTest(Test_parse('test_profile_mini'))#full test
	#private method
	#suite.addTest(Test_parse('test_get_birth'))#full test
	#suite.addTest(Test_parse('test_get_gender'))#full test
	#suite.addTest(Test_parse('test_split_high_edu'))#full test
	#suite.addTest(Test_parse('test_split_low_edu'))#full test
	suite.addTest(Test_parse('test_sub_space'))#full test
	#suite.addTest(Test_parse('test_drop_link'))
	#suite.addTest(Test_parse('test_drop_pf_extra'))
	#suite.addTest(Test_parse('test_drop_href'))
	#suite.addTest(Test_parse('test_drop_span'))
	#suite.addTest(Test_parse('test_drop_rrurl'))
	#suite.addTest(Test_parse('test_split_owner'))
	runner=unittest.TextTestRunner()
	runner.run(suite)
