import unittest
import parse
from download import download

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
			None]
		names=[
			{'6754031':'王瑛','331442':'En.王哲'},
			{'9439171':''},
			{'34134':'～@%……'},
			dict(),
			None,
			None]
		for pfHref,name in zip(pfHrefs,names):
			self.assertEquals(parse.friendList(pfHref),name)

	def test_profile_detail(self):
		contents={"""<dl class="info"><dt>性别:</dt><dd>女</dd><dt>生日 :</dt>
			<dd><a stats="info_info" class="pop-module-mark"ref=pf_birth'>1994</a> 年\t\\t\n\\n
			<a stats="info_info"href="http://page.renren.com/600002589?ref=pf_star">摩羯座</a>
			</dd><dt>家乡 :</dt><dd><span class="link">陕西</span><span>延安市</span></dd>\t\t\t\t</dl>""":{'性别':'女','生日':'1994 年摩羯座','家乡':'陕西延安市'},#full items with all kinds of element
			"""<dl class="info"><dt>性别 :</dt><dd></dd></dl>""":{'性别':''},#value none
			"""<dl class="info"></dl>""":{},#no items
			None:None}
		for  content,expt in contents.items():
			self.assertEquals(parse.profile_detail(content),expt)

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

	def test_split_tlbirth(self):
		births={"""男生，2月13日""":('男生', '2月13日'),#cn comma, success
			"""女生,2月13日""":('女生', '2月13日'),#en comma,success
			"""男生2月13日""":(None,"src=男生2月13日,res=['男生2月13日']"),#no comma,return None and cause
			"""男生 ， 2月13日""":('男生', '2月13日'),#cn comma with space
			"""男生 , 2月13日""":('男生', '2月13日'),#en comma with space
			""" 男生 ， 正月 十七日""":('男生', '正月 十七日'),#chinese birth
			None:None
		}
		for birth,expt in births.items():
			self.assertEquals(parse.split_tlbirth(birth),expt)

	def test_drop_href(self):
		contents={"""<dt>生日\n\\n\t\\t :</dt><dd><a stats="info'> 1994\n\\n\t\\t </a> 年\n\\n\t\\t <a href="pf_star">摩羯座</a><a stats="info_info">陕西</a> \t\\t\n\\n """:"""<dt>生日\n\\n\t\\t :</dt><dd> 1994\n\\n\t\\t  年\n\\n\t\\t 摩羯座陕西 \t\\t\n\\n """,#all kinds of elements in and out <a></a>
		"""hello<dt>birth</dt>""":"""hello<dt>birth</dt>""",#no href
		"""<about>hello</about>""":"""<about>hello</about>""",#start with <a,but not href
		None:None
		}
		for content,expt in contents.items():
			self.assertEquals(parse.drop_href(content),expt)

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
	suite.addTest(Test_parse('test_friendList'))
	suite.addTest(Test_parse('test_profile_detail'))
	suite.addTest(Test_parse('test_homepage_tl'))
	suite.addTest(Test_parse('test_homepage_basic_privacy'))
	#private method
	suite.addTest(Test_parse('test_split_tlbirth'))
	suite.addTest(Test_parse('test_drop_href'))
	suite.addTest(Test_parse('test_drop_span'))
	suite.addTest(Test_parse('test_drop_rrurl'))
	suite.addTest(Test_parse('test_split_owner'))
	#suite.addTest(Test_parse('test_drop_space'))
	#suite.addTest(Test_parse('test_drop_extra'))
	runner=unittest.TextTestRunner()
	runner.run(suite)
