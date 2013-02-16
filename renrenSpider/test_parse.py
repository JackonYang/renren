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
		contents={"""<dt>性别:</dt><dd>女</dd>,<dt>生日 :</dt><dd><a st>1998</a>年<a st>2</a>月<a st>13</a>日<a st>水瓶座</a></dd>,<dt>家乡 :</dt><dd><a st>内蒙古</a><a st>呼伦贝尔市</a></dd>,<dt>大学 :</dt><dd><a st>北京中医药大学</a>-<a st>2013年</a>-<a st>东方学院</a><br><a st>北京理工大学</a>-<a st>2011年</a>-<a st>生命科学与技术学院六院</a><br></dd>,<dt>高中 :</dt><dd><a st>北京二十五中</a>-<a st>1997年</a><a st>烟台二中</a>-<a st>2004年</a></dd>,<dt>初中:</dt><dd><a st>一个初中</a>-<a st>1995年</a><a st>烟台二中</a>-<a st>2014年</a></dd>,<dt>小学:</dt><dd><a st>一个小学</a>-<a st>1991年</a><a st>青岛二小</a>-<a st>2001年</a></dd>""":{'edu_college': {('北京中医药大学', '2013', '东方学院'), ('北京理工大学', '2011', '生命科学与技术学院六院')}, 'edu_primary': {('一个小学', '1991'), ('青岛二小', '2001')}, 'hometown': '内蒙古呼伦贝尔市', 'birth_month': '2', 'edu_senior': {('烟台二中', '2004'), ('北京二十五中', '1997')}, 'edu_junior': {('烟台二中', '2014'), ('一个初中', '1995')}, 'gender': 'f', 'birth_day': '13', 'birth_year': '1998'},#full items and no space
			"""<dt> 性别 : </dt> <dd> 女 </dd> , <dt> 生日 : </dt> <dd> <a st> 1998 </a> 年 <a st> 2 </a> 月 <a st> 13 </a> 日 <a st> 水瓶座 </a> </dd> , <dt> 家乡 :</dt>\n<dd>\n<a st>\n内蒙古\n</a>\n<a st>\n呼伦贝尔市\n</a>\n</dd>\n,\n\n<dt> 大学 :</dt>\n\n<dd>\n\n<a st>\n\n北京中医药大学\n</a>-<a st>\n 2013年\n </a>-<a st>东方学院</a><br><a st>北京理工大学\t\t</a>-<a st>2011年</a>-<a st>生命科学与技术学院六院</a><br></dd>,<dt>高中 :</dt><dd><a st>北京二十五中</a>-<a st>1997年</a><a st>烟台二中</a>-<a st>2004年</a></dd>,<dt>初中:</dt><dd><a st>一个初中</a>-<a st>1995年</a><a st>烟台二中</a>-<a st>2014年</a></dd>,<dt>小学:</dt><dd><a st>一个小学</a>-<a st>1991年</a><a st>青岛二小</a>-<a st>2001年</a></dd>""":{'edu_college': {('北京中医药大学', '2013', '东方学院'), ('北京理工大学', '2011', '生命科学与技术学院六院')}, 'edu_primary': {('一个小学', '1991'), ('青岛二小', '2001')}, 'hometown': '内蒙古 呼伦贝尔市', 'birth_month': '2', 'edu_senior': {('烟台二中', '2004'), ('北京二十五中', '1997')}, 'edu_junior': {('烟台二中', '2014'), ('一个初中', '1995')}, 'gender': 'f', 'birth_day': '13', 'birth_year': '1998'},#full items and space and \n \t
			"""<dt>生日 :</dt><dd><a st>1998</a>年<a st>2</a>月<a st>13</a>日</dd>""":{'birth_day':'13','birth_year':'1998','birth_month':'2','edu_college': None,'edu_junior': None,'edu_primary': None,'edu_senior': None,'gender': None,'hometown':''},#birth only
			"""<dt>家乡 :</dt><dd><a st>内蒙古</a><a st>呼伦贝尔市</a></dd>""":{'hometown':'内蒙古呼伦贝尔市','birth_day': None,'birth_month': None,'birth_year': None,'edu_college': None,'edu_junior': None,'edu_primary': None,'edu_senior': None,'gender': None},#hometown only
			"""<dt>大学 :</dt><dd><a st>北京中医药大学</a>-<a st>2013年</a>-<a st>东方学院</a><br><a st>北京理工大学</a>-<a st>2011年</a>-<a st>生命科学与技术学院六院</a><br></dd>""":{'edu_college': {('北京中医药大学', '2013', '东方学院'), ('北京理工大学', '2011', '生命科学与技术学院六院')},'birth_day': None,'birth_month': None,'birth_year': None,'edu_junior': None,'edu_primary': None,'edu_senior': None,'gender': None,'hometown':''}#edu info only
			}
		for  content,expt in contents.items():
			self.assertEquals(parse.profile_detail(content.split(',')),expt)

	def test_homepage_tl(self):
		contents={"""<ul class="information-ul" id="information-ul" onclick href='http:'">\\n\n\t\\t<li class="school"><span>就读于西北大学</span></li>\n\t<li class="birthday">\n<span class="link">男生</span>\\n\n<span>，2月13日</span>\t\\t</li><li class="hometown">来自内蒙古<a stats="info_info">延安市</a></li><li class="address">现居\\n山南地区</li></ul>""":{'school':'就读于西北大学','gender':'男生','birth':'2月13日','hometown':'来自内蒙古延安市','address':'现居山南地区'},#full items with all kinds of element
			"""<ul class="information-ul" id="information-ul" onclick href='http:'">\t\\t\n\\n</ul>""":{},#no items
			None:None
			}
		for content,expt in contents.items():
			self.assertEquals(parse.homepage_tl(content),expt)

	def test_homepage_basic_privacy(self):
		contents={"""<ul class="user-info clearfix"><li class="gender"><span class="link">男生</span></li>\t\\t\n\\n
			<li class="hometown">来自<span>山东</span> <a href="">烟台市\t\\t\n\\n</a><span class="link">New Work</span></li>
			<li class="school">在<span class="link">Fachhochschule Aachen</span>读书</li></ul>""":{'gender':'男生','hometown':'来自山东 烟台市New Work','school':'在Fachhochschule Aachen读书'},#all kinds of items
			"""<ul class="user-info clearfix"></ul>""":{},#no items
			None:None}
		for content,expt in contents.items():
				self.assertEquals(parse.homepage_basic_privacy(content),expt)

#basic
	def test_get_birth(self):
		contents={'80 后 10 月 12 日天秤座':{'birth_day': '12', 'birth_month': '10', 'birth_year': '80'},# xx后 and int(2)
				'2012年8月1日狮子座':{'birth_day': '1', 'birth_month': '8', 'birth_year': '2012'},# xx年 and int(1)
				' 3 月 6 日 双鱼座':{'birth_day': '6', 'birth_month': '3', 'birth_year': None},#no age info
				'1987年9月1日':{'birth_day': '1', 'birth_month': '9', 'birth_year': '1987'},#no star info
				'3 月 29 日':{'birth_day': '29', 'birth_month': '3', 'birth_year': None},#no age or star info
				'3-29':{'birth_day': '29', 'birth_month': '3', 'birth_year': None},#no age or star info
				'3 - 31':{'birth_day': '31', 'birth_month': '3', 'birth_year': None},#no age or star info
				'2011-9-1':{'birth_day': '1', 'birth_month': '9', 'birth_year': '2011'},#no star info
				'1993 - 9 - 1':{'birth_day': '1', 'birth_month': '9', 'birth_year': '1993'},#no star info
				'no match':{'birth_year':None,'birth_month':None,'birth_day':None},
				None:{'birth_year':None,'birth_month':None,'birth_day':None}
				}
		for content,expt in contents.items():
			self.assertEquals(parse._get_birth(content),expt)
	def test_get_gender(self):
		contents={'他是男生':'m','男生':'m','她是女生':'f','女生':'f','女':'f','男':'m','no match':None,None:None}
		for content,expt in contents.items():
			self.assertEquals(parse._get_gender(content),expt)

#edu
	def test_split_high_edu(self):
		contents={' Birmingam City - 2011 年 - 其它院系 <br> 西北大学 - 2012 年 - 其它院系 <br> ':{('Birmingam City', '2011', '其它院系'), ('西北大学', '2012', '其它院系')},#full space
				'Birmingam City-2011年-其它院系<br>西北大学-2012年-其它院系<br>':{('Birmingam City', '2011', '其它院系'), ('西北大学', '2012', '其它院系')},#no space
				'西北大学-2010年-物理学系<br>':{('西北大学', '2010', '物理学系')},
				'Lincoln University - 1970年 <br>':{('Lincoln University', '1970')},
				None:None
				}
		for content,expt in contents.items():
			self.assertEquals(parse._split_high_edu(content),expt)
	def test_split_low_edu(self):
		contents={' 万州上海中学 - 2009年 万州高级中学 - 2012年 ':{('万州高级中学', '2012'), ('万州上海中学', '2009')},#full space
				'万州上海中学-2004年万州高级中学-2011年':{('万州高级中学', '2011'), ('万州上海中学', '2004')},#no space
				'三原县南郊中学- 2005年':{('三原县南郊中学', '2005')}}#one item
		for content,expt in contents.items():
			self.assertEquals(parse._split_low_edu(content),expt)

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
	#suite.addTest(Test_parse('test_friendList'))
	#suite.addTest(Test_parse('test_homepage_tl'))
	#suite.addTest(Test_parse('test_homepage_basic_privacy'))

	#checked
	suite.addTest(Test_parse('test_profile_detail'))#full test
	#private method
	suite.addTest(Test_parse('test_get_birth'))#full test
	suite.addTest(Test_parse('test_get_gender'))#full test
	suite.addTest(Test_parse('test_split_high_edu'))#full test
	suite.addTest(Test_parse('test_split_low_edu'))#full test
	#suite.addTest(Test_parse('test_drop_href'))
	#suite.addTest(Test_parse('test_drop_span'))
	#suite.addTest(Test_parse('test_drop_rrurl'))
	#suite.addTest(Test_parse('test_split_owner'))
	#suite.addTest(Test_parse('test_drop_space'))
	#suite.addTest(Test_parse('test_drop_extra'))
	runner=unittest.TextTestRunner()
	runner.run(suite)
