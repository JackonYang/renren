import pymysql

class repo_mysql:
	def __init__(self,namePre='test'):
		self.namePre=namePre
		self.table=dict()
		self.conn=self._getConn()
		self.cur=self.conn.cursor()
		self._init_table('history')
	def __del__(self):
		self.cur.close()
		self.conn.close()

	def save_friendList(self,record,rid,run_info=None):
		"""save record and return rows affected.save nothing if empty.
		return None if input error"""
		if record is None:
			return None
		elif not isinstance(record,dict):
			return None
		elif record == {}:
			return 0
		pageStyle='friendList'
		if pageStyle not in self.table:
			self._init_table(pageStyle)
		if 'name' not in self.table:
			self._init_table('name')
		val_relation='),({},'.format(rid).join(record.keys())
		sql_relation='insert into {} (renrenId1,renrenId2) values ({},{})'.format(self.table[pageStyle],rid,val_relation)
		val_name=str(set(record.items())).strip('{}')
		sql_name='insert into {} (renrenId1,name) values {}'.format(self.table['name'],val_name)
		try:
			n=self.cur.execute(sql_relation)
			self.cur.execute(sql_name)
		except Exception as e:
			print(e)
			print(sql_relation)
			print(sql_name)
			return None
		else:
			self.conn.commit()
			if run_info is not None:
				self.save_history(rid,pageStyle,run_info,len(record))
			return n

	def save_status(self,record,rid=None,run_info=None):
		if record is None:
			return None
		elif not isinstance(record,dict):
			return None
		elif record == {}:
			return 0
		pageStyle='status'
		if pageStyle not in self.table:
			self._init_table(pageStyle)
		saved=0
		for statusId,stat in record.items():
			val_stat="statusId='{}'".format(statusId)
			for tag,value in stat.items():
				if value is not None:
					value=value.replace("'","\\'").rstrip('\\')#format , and \ 
				val_stat += ",{}='{}'".format(tag,value)
			sql_stat='insert into {} set {}'.format(self.table[pageStyle],val_stat)
			try:
				saved += self.cur.execute(sql_stat)
			except Exception as e:
				print(sqlStat)
				return None
		self.conn.commit()
		if run_info is not None:
			self.save_history(rid,pageStyle,run_info,len(record))
		return saved

	def save_profile(self,record,rid):
		"""save profile and return rows affected.return None if input error"""
		if record is None:
			return None
		elif not isinstance(record,dict):
			return None
		elif record == {}:
			return 0
		pageStyle='profile'
		val_pf="renrenId1='{}'".format(rid)
		for tag,value in record.items():
			val_pf += ",{}='{}'".format(pf_cols.get(tag,'extra'),value)
		sql_pf='insert into {} set {}'.format(self.tempTable[pfStyle],val_pf)
		try:
			n=self.cur.execute(sql_pf)
		except Exception as e:
			print(sql_pf)
			return None
		else:
			self.conn.commit()
			return n

	def save_history(self,rid,pageStyle,run_info,n_record):
		sql_log="insert into {} (rid,page_style,run_info,n_record) values('{}','{}','{}','{}')".format(self.table['history'],rid,pageStyle,run_info,n_record)
		n=self.cur.execute(sql_log)
		self.conn.commit()
		return n

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

	def _init_table(self,pageStyle):
		self.table[pageStyle]='{}_{}'.format(self.namePre,pageStyle)
		self.cur.execute(sqls[pageStyle].format(self.table[pageStyle],key[pageStyle]))
		self.conn.commit()

	def _getConn(self,usr='root',passwd='Kunth123',db='data_bang'):
		return pymysql.connect(host='127.0.0.1',port=3306,user=usr,passwd=passwd,db=db,charset='utf8')

pf_cols={
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
sqls=dict()
sqls['name']='CREATE TABLE if not exists {} (renrenId1 varchar(15) NOT NULL,name varchar(20),lastmodified TIMESTAMP DEFAULT NOW() {})ENGINE=InnoDB DEFAULT CHARSET = utf8 COLLATE = utf8_unicode_ci;'
sqls['friendList']='CREATE TABLE if not exists {} (renrenId1 varchar(15) NOT NULL,renrenId2 varchar(15) NOT NULL,KEY one(renrenId1),KEY two(renrenId2),lastmodified TIMESTAMP DEFAULT NOW() {} )ENGINE = InnoDB DEFAULT CHARSET = utf8 COLLATE = utf8_unicode_ci;'
sqls['profile_detail']='CREATE TABLE if not exists {} (renrenId1 varchar(20) NOT NULL,'+' varchar(100),'.join(set(pf_cols.values()))+' varchar(100),lastmodified TIMESTAMP DEFAULT NOW() {})ENGINE=InnoDB DEFAULT CHARSET = utf8;'
sqls['profile_mini']='CREATE TABLE if not exists {} (renrenId1 varchar(20) NOT NULL,'+' varchar(100),'.join(set(pf_mini.values()))+' varchar(100),lastmodified TIMESTAMP DEFAULT NOW() {})ENGINE=InnoDB DEFAULT CHARSET = utf8;'
sqls['profile_empty']='CREATE TABLE if not exists {} (renrenId1 varchar(20) NOT NULL,pfStyle varchar(20),lastmodified TIMESTAMP DEFAULT NOW() {})ENGINE=InnoDB DEFAULT CHARSET = utf8;'
sqls['status']='CREATE TABLE if not exists {} (statusId varchar(20) NOT NULL,renrenId1 varchar(20),timestamp varchar(20),cur_name varchar(50),cur_content varchar(500),orig_owner varchar(20),orig_name varchar(50),orig_content varchar(500),lastmodified TIMESTAMP DEFAULT NOW(),KEY cur_owner(renrenId1),KEY orig_owner(orig_owner) {})ENGINE=InnoDB DEFAULT CHARSET = utf8;'
sqls['history']='CREATE TABLE if not exists {}(rid varchar(15), page_style varchar(15),n_record varchar(8),run_info varchar(50) {}) ENGINE  = InnoDB  DEFAULT CHARSET  = utf8;'
key={'name':',KEY idx_temp(renrenId1)','friendList':',KEY idx_temp (renrenId1,renrenId2)','profile_detail':',KEY (renrenId1)','status':',key (statusId)','profile_mini':',KEY (renrenId1)','profile_empty':',KEY (renrenId1)','history':''}
#primary={'name':',PRIMARY KEY (renrenId1)','profile_detail':',PRIMARY KEY (renrenId1)','profile_mini':',PRIMARY KEY (renrenId1)','profile_empty':',PRIMARY KEY (renrenId1)','friendList':',PRIMARY KEY (renrenId1,renrenId2)','status':',PRIMARY KEY (statusId)'}
