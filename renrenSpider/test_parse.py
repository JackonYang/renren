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
		expt={'性别':'女','生日':'1994 年摩羯座','家乡':'陕西延安市'}#full items with all kinds of element
		contents=['<dt>性别:</dt><dd>女</dd>',
				"""<dt>生日 :</dt>\n<dd><a stats="info_info" ref=pf_birth'>1998</a> 年\n<a stats="info_info">2</a> 月 <a stats="info_info">13</a> 日<!-- <a class="pop-module-mark">水瓶座</a> -->\n<a stats="info_info" ref=pf_star">水瓶座</a>\n</dd>""",
			"""<dt>家乡 :</dt>\n<dd>\n<a stats="info_info"ref=pf_hometown">内蒙古</a> <a stats="info_info"ref=pf_hometown">呼伦贝尔市</a>\n</dd>""",
			"""<dt>大学 :</dt>
			<dd>
			<a stats="info_info" class="pop-module-mark" k="{title:'同学们常去',type:4,key:'北京中医药大学',showPages:3,ref:'pf_spread' }" href='http://browse.renren.com/searchEx.do?s=0&amp;p=%5B%7B%22id%22%3A%221023%22%2C%22t%22%3A%22univ%22%2C%22name%22%3A%22%E5%8C%97%E4%BA%AC%E4%B8%AD%E5%8C%BB%E8%8D%AF%E5%A4%A7%E5%AD%A6%22%7D%5D&amp;ref=pf_spread'>北京中医药大学</a>
			- <a stats="info_info" class="pop-module-mark" k="{title:'同学们常去',type:4,key:'2013级',showPages:3,ref:'pf_spread' }" href='http://browse.renren.com/searchEx.do?s=0&amp;p=[{"id":"1023","t":"univ","year":"2013","name":"%E5%8C%97%E4%BA%AC%E4%B8%AD%E5%8C%BB%E8%8D%AF%E5%A4%A7%E5%AD%A6"}]&amp;ref=pf_spread'>2013年</a>- <a stats="info_info" class="pop-module-mark" k="{title:'同学们常去',type:4,key:'东方学院',showPages:3,ref:'pf_spread' }" href='http://browse.renren.com/searchEx.do?s=0&amp;p=%5B%7B%22id%22%3A%221023%22%2C%22t%22%3A%22univ%22%2C%22depa%22%3A%22%E4%B8%9C%E6%96%B9%E5%AD%A6%E9%99%A2%22%2C%22name%22%3A%22%E5%8C%97%E4%BA%AC%E4%B8%AD%E5%8C%BB%E8%8D%AF%E5%A4%A7%E5%AD%A6%22%7D%5D&amp;ref=pf_spread'>东方学院</a><br><a stats="info_info" class="pop-module-mark" k="{title:'同学们常去',type:4,key:'北京理工大学',showPages:3,ref:'pf_spread' }" href='http://browse.renren.com/searchEx.do?s=0&amp;p=%5B%7B%22id%22%3A%221011%22%2C%22t%22%3A%22univ%22%2C%22name%22%3A%22%E5%8C%97%E4%BA%AC%E7%90%86%E5%B7%A5%E5%A4%A7%E5%AD%A6%22%7D%5D&amp;ref=pf_spread'>北京理工大学</a>
			- <a stats="info_info" class="pop-module-mark" k="{title:'同学们常去',type:4,key:'2011级',showPages:3,ref:'pf_spread' }" href='http://browse.renren.com/searchEx.do?s=0&amp;p=[{"id":"1011","t":"univ","year":"2011","name":"%E5%8C%97%E4%BA%AC%E7%90%86%E5%B7%A5%E5%A4%A7%E5%AD%A6"}]&amp;ref=pf_spread'>2011年</a>- <a stats="info_info" class="pop-module-mark" k="{title:'同学们常去',type:4,key:'生命科学与技术学院六院',showPages:3,ref:'pf_spread' }" href='http://browse.renren.com/searchEx.do?s=0&amp;p=%5B%7B%22id%22%3A%221011%22%2C%22t%22%3A%22univ%22%2C%22depa%22%3A%22%E7%94%9F%E5%91%BD%E7%A7%91%E5%AD%A6%E4%B8%8E%E6%8A%80%E6%9C%AF%E5%AD%A6%E9%99%A2%E5%85%AD%E9%99%A2%22%2C%22name%22%3A%22%E5%8C%97%E4%BA%AC%E7%90%86%E5%B7%A5%E5%A4%A7%E5%AD%A6%22%7D%5D&amp;ref=pf_spread'>生命科学与技术学院六院</a><br></dd><dt>高中 :</dt>
			<dd>
			<a stats="info_info" class="pop-module-mark" k="{title:'同学们常去',type:4,key:'北京二十五中',showPages:3,ref:'pf_spread' }" href='http://browse.renren.com/searchEx.do?s=0&amp;p=%5B%7B%22t%22%3A%22high%22%2C%22name%22%3A%22%E5%8C%97%E4%BA%AC%E4%BA%8C%E5%8D%81%E4%BA%94%E4%B8%AD%22%7D%5D&amp;ref=pf_spread'>北京二十五中</a>
			- <a stats="info_info" class="pop-module-mark" k="{title:'同学们常去',type:4,key:'1997级',showPages:3 }" href='http://browse.renren.com/searchEx.do?s=0&amp;p=%5B%7B%22t%22%3A%22high%22%2C%22year%22%3A%221997%22%2C%22name%22%3A%22%E5%8C%97%E4%BA%AC%E4%BA%8C%E5%8D%81%E4%BA%94%E4%B8%AD%22%7D%5D&amp;ref=pf_spread'>1997年</a>

			<a stats="info_info" class="pop-module-mark" k="{title:'同学们常去',type:4,key:'北京二十一中',showPages:3,ref:"""
			]
			#"""<dl class="info"><dt>性别 :</dt><dd></dd></dl>""":{'性别':''},#value none
			#"""<dl class="info"></dl>""":{},#no items
			#None:None}
		#for  content,expt in zip(contents,expt):
			#self.assertEquals(parse.profile_detail(content),expt)
		print(parse.profile_detail(contents))

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
				'no match':None,
				None:None
				}
		for content,expt in contents.items():
			self.assertEquals(parse._get_birth(content),expt)
	def test_get_gender(self):
		contents={'他是男生':'m','男生':'m','她是女生':'f','女生':'f','女':'f','男':'m','no match':None,None:None}
		for content,expt in contents.items():
			self.assertEquals(parse._get_gender(content),expt)
	def test_split_high_edu(self):
		contents={'Birmingam City- 2011年- 其它院系<br>Birmingam City- 2012年- 其它院系<br>':{('Birmingam City', '2011', '其它院系'), ('Birmingam City', '2012', '其它院系')},
				'西北大学- 2010年- 物理学系<br>':{('西北大学', '2010', '物理学系')},
				'Lincoln University- 1970年<br>':{('Lincoln University', '1970')},
				'Iowa State University- 2008年- 其它院系<br>':{('Iowa State University', '2008', '其它院系')}
				}
		for content,expt in contents.items():
			self.assertEquals(parse._split_high_edu(content),expt)
	def test_split_low_edu(self):
		contents={'万州上海中学- 2009年 万州高级中学- 2012年':{('万州高级中学', '2012'), ('万州上海中学', '2009')},
				'三原县南郊中学- 2005年':{('三原县南郊中学', '2005')}}
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
	#suite.addTest(Test_parse('test_profile_detail'))
	#suite.addTest(Test_parse('test_homepage_tl'))
	#suite.addTest(Test_parse('test_homepage_basic_privacy'))
	#private method
	suite.addTest(Test_parse('test_get_birth'))#full test
	suite.addTest(Test_parse('test_get_gender'))#full test
	#suite.addTest(Test_parse('test_split_high_edu'))
	#suite.addTest(Test_parse('test_split_low_edu'))
	#suite.addTest(Test_parse('test_drop_href'))
	#suite.addTest(Test_parse('test_drop_span'))
	#suite.addTest(Test_parse('test_drop_rrurl'))
	#suite.addTest(Test_parse('test_split_owner'))
	#suite.addTest(Test_parse('test_drop_space'))
	#suite.addTest(Test_parse('test_drop_extra'))
	runner=unittest.TextTestRunner()
	runner.run(suite)
