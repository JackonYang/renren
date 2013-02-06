import pymysql
pf_details={
	#basic$
	'生日':'birth','家乡':'hometown','性别':'gender',
	#edu
	'大学':'edu_college','高中':'edu_senior','中专技校':'edu_tech','初中':'edu_junior','小学':'edu_primary',
	#work
	'公司':'company','时间':'work_time',
	#contact
	'QQ':'qq','MSN':'msn','手机号':'phone','个人网站':'personal_website','我的域名':'domain1','个性域名':'domain2'
}
pf_mini={'location':'nowCity','address':'nowCity','work':'nowCompany','school':'nowSchool','birth':'birth','hometown':'hometown','gender':'gender'}

class database:
	sqls=dict()
	sqls['name']='CREATE TABLE if not exists {} (renrenId1 varchar(15) NOT NULL,name varchar(20),lastmodified TIMESTAMP DEFAULT NOW() {})ENGINE=InnoDB DEFAULT CHARSET = utf8 COLLATE = utf8_unicode_ci;'
	sqls['friendList']='CREATE TABLE if not exists {} (renrenId1 varchar(15) NOT NULL,renrenId2 varchar(15) NOT NULL,KEY one(renrenId1),KEY two(renrenId2),lastmodified TIMESTAMP DEFAULT NOW() {} )ENGINE = InnoDB DEFAULT CHARSET = utf8 COLLATE = utf8_unicode_ci;'
	sqls['profile_detail']='CREATE TABLE if not exists {} (renrenId1 varchar(20) NOT NULL,'+' varchar(100),'.join(set(pf_details.values()))+' varchar(100),lastmodified TIMESTAMP DEFAULT NOW() {})ENGINE=InnoDB DEFAULT CHARSET = utf8;'
	sqls['profile_mini']='CREATE TABLE if not exists {} (renrenId1 varchar(20) NOT NULL,'+' varchar(100),'.join(set(pf_mini.values()))+' varchar(100),lastmodified TIMESTAMP DEFAULT NOW() {})ENGINE=InnoDB DEFAULT CHARSET = utf8;'
	sqls['profile_empty']='CREATE TABLE if not exists {} (renrenId1 varchar(20) NOT NULL,pfStyle varchar(20),lastmodified TIMESTAMP DEFAULT NOW() {})ENGINE=InnoDB DEFAULT CHARSET = utf8;'
	sqls['status']='CREATE TABLE if not exists {} (statusId varchar(20) NOT NULL,renrenId1 varchar(20),timestamp varchar(20),cur_name varchar(50),cur_content varchar(500),orig_owner varchar(20),orig_name varchar(50),orig_content varchar(500),lastmodified TIMESTAMP DEFAULT NOW(),KEY cur_owner(renrenId1),KEY orig_owner(orig_owner) {})ENGINE=InnoDB DEFAULT CHARSET = utf8;'
	key={'name':',KEY idx_temp(renrenId1)','friendList':',KEY idx_temp (renrenId1,renrenId2)','profile_detail':',KEY (renrenId1)','status':',key (statusId)','profile_mini':',KEY (renrenId1)','profile_empty':',KEY (renrenId1)'}
	primary={'name':',PRIMARY KEY (renrenId1)','profile_detail':',PRIMARY KEY (renrenId1)','profile_mini':',PRIMARY KEY (renrenId1)','profile_empty':',PRIMARY KEY (renrenId1)','friendList':',PRIMARY KEY (renrenId1,renrenId2)','status':',PRIMARY KEY (statusId)'}

	def __init__(self,namePre='test'):
		self.conn=pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='Kunth123',db='data_bang',charset='utf8')
		self.cur=self.conn.cursor()
		self.mainTable=dict()
		self.tempTable=dict()
		for table in self.sqls.keys(): 
			self.mainTable[table]='{}_main_{}'.format(namePre,table)
			self.tempTable[table]='{}_temp_{}'.format(namePre,table)
		self.createTempTable()
		self.createMainTable()
	def close(self):
		self.conn.close()
		self.cur.close()

	def friendList(self,renrenId,names):
		"""insert into db, and return rows affected.return None if input error"""
		if names is None:
			return None
		elif not isinstance(names,dict):
			return None
		elif names == {}:
			return 0
		valFl='),({},'.format(renrenId).join(names.keys())
		sqlFl='insert into {} (renrenId1,renrenId2) values ({},{})'.format(self.tempTable['friendList'],renrenId,valFl)
		valNm=str(set(names.items())).strip('{}')
		sqlNm='insert into {} (renrenId1,name) values {}'.format(self.tempTable['name'],valNm)
		try:
			n=self.cur.execute(sqlFl)
			self.cur.execute(sqlNm)
		except Exception as e:
			print(sqlFl)
			print(sqlNm)
			return None
		else:
			self.conn.commit()
			return n

	def profile(self,renrenId,pf,pfStyle):
		"""insert into db, and return rows affected.return None if input error"""
		if pf is None:
			return None
		elif not isinstance(pf,dict):
			return None
		elif pf == {}:
			return 0
		valPf="renrenId1='{}'".format(renrenId)
		if pfStyle == 'profile_detail':
			for tag,value in pf.items():
				valPf += ",{}='{}'".format(pf_details[tag],value)
		elif pfStyle == 'profile_mini':
			for tag,value in pf.items():
				valPf += ",{}='{}'".format(pf_mini[tag],value)
		else:
			return None
		sqlPf='insert into {} set {}'.format(self.tempTable[pfStyle],valPf)
		try:
			n=self.cur.execute(sqlPf)
		except Exception as e:
			print(sqlPf)
			return None
		else:
			self.conn.commit()
			return n

	def status(self,stats):
		if stats is None:
			return None
		elif not isinstance(stats,dict):
			return None
		elif stats == {}:
			return 0
		saved=0
		for statusId,stat in stats.items():
			valStat="statusId='{}'".format(statusId)
			for tag,value in stat.items():
				if value is not None:
					value=value.replace("'","\\'").rstrip('\\')
				valStat += ",{}='{}'".format(tag,value)
			sqlStat='insert into {} set {}'.format(self.tempTable['status'],valStat)
			try:
				saved += self.cur.execute(sqlStat)
			except Exception as e:
				print(sqlStat)
				return 0
		self.conn.commit()
		return saved

	def profile_empty(self,renrenId,pfStyle):
		sqlPf="insert into {} set renrenId1='{}',pfStyle='{}'".format(self.tempTable['profile_empty'],renrenId,pfStyle)
		try:
			n=self.cur.execute(sqlPf)
		except Exception as e:
			print(sqlPf)
			return None
		else:
			self.conn.commit()
			return n

	def getFriendList(self,renrenId):
		return self._getRenrenId(2,renrenId)

	def _getRenrenId(self,col,renrenId):
		target=str(col)
		where=str(col%2+1)
		res=set()
		for table in [self.mainTable['friendList'],self.tempTable['friendList']]:
			self.cur.execute("SELECT renrenId{} FROM {} where renrenId{}={}".format(target,table,where,renrenId))
			for item in self.cur.fetchall():
				res.add(item[0])
		return res
	def getSearched(self,pageStyle):
		if pageStyle=='profile':
			tables={self.mainTable['profile_detail'],self.tempTable['profile_detail'],self.mainTable['profile_mini'],self.tempTable['profile_mini'],self.mainTable['profile_empty'],self.tempTable['profile_empty']}
		else:
			tables={self.mainTable[pageStyle],self.tempTable[pageStyle]}
		res=set()
		for table in tables:
			self.cur.execute("SELECT renrenId1 FROM {} group by renrenId1".format(table))
			for item in self.cur.fetchall():
				res.add(item[0])
		return res

	def createTempTable(self):
		for attr in self.sqls.keys():
			self.cur.execute(self.sqls[attr].format(self.tempTable[attr],self.key[attr]))
			#print(self.sqls[attr].format(self.tempTable[attr],self.key[attr]))
	def createMainTable(self):
		for attr in self.sqls.keys():
			self.cur.execute(self.sqls[attr].format(self.mainTable[attr],self.primary[attr]))
	def dropTempTable(self):
		for table in self.tempTable.values():
			self.cur.execute('drop table if exists {}'.format(table))
