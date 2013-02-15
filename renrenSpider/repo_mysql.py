import pymysql

cfg_filename='db_renren.ini'

class repo_mysql:
	def __init__(self,table_pre='test'):
		self.table={}
		self.table_pre=table_pre
		self.conn=self._getConn()
		self.cur=self.conn.cursor()
		self._init_table('history')
	def __del__(self):
		self.cur.close()
		self.conn.close()

	def save_friendList(self,record,rid,run_info=None):
		"""save record and return rows affected.save nothing if empty.
		return None if input error"""
		return self._save_process('friendList',record,rid,run_info)
	def save_status(self,record,rid,run_info=None):
		"""save record and return rows affected.save nothing if empty.
		return None if input error"""
		return self._save_process('status',record,rid,run_info)

	def save_profile(self,record,rid):
		"""save profile and return rows affected.return None if input error"""
		if not isinstance(record,dict):
			return None
		if record == {}:
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

	def _save_process(self,pageStyle,record,rid,run_info):
		"""save record and return rows affected.save nothing if empty.
		return None if input error"""
		if not isinstance(record,dict):
			return None
		sql_meth=getattr(self,'_sql_{}'.format(pageStyle))
		sqls=sql_meth(record,rid)
		n=0
		if run_info is not None:
			n -= 1
			sqls.append(self.sql_history(rid,pageStyle,run_info,len(record)))
		try:
			for sql in sqls:
				n += self.cur.execute(sql)
			self.conn.commit()
		except Exception as e:
			print(e)
			print(sqls)
		return self.count(n,pageStyle)

	def getSearched(self,pageStyle):
		#only success download is logged
		res=set()
		self.cur.execute("SELECT rid FROM {} where page_style='{}'".format(self.table['history'],pageStyle))
		for item in self.cur.fetchall():
			res.add(item[0])
		return res

	def getFriendList(self,renrenId):
		return self._getRenrenId(2,renrenId)

	def _getRenrenId(self,col,renrenId):
		pageStyle='friendList'
		if pageStyle not in self.table:
			self._init_table(pageStyle)
		target=str(col)
		where=str(col%2+1)
		res=set()
		self.cur.execute("SELECT renrenId{} FROM {} where renrenId{}={}".format(target,self.table[pageStyle],where,renrenId))
		for item in self.cur.fetchall():
			res.add(item[0])
		return res

	def _init_table(self,pageStyle):
		self.cur.execute(self.sql_create_table(pageStyle))
		self.conn.commit()
		self.table[pageStyle]='{}_{}'.format(self.table_pre,pageStyle)

	def _getConn(self,usr='root',passwd='Kunth123',db='data_bang'):
		return pymysql.connect(host='127.0.0.1',port=3306,user=usr,passwd=passwd,db=db,charset='utf8')

	def sql_create_table(self,pageStyle):
		import configparser
		config=configparser.ConfigParser()
		config.read(cfg_filename)
		if pageStyle in config.sections():
			col=''
			for key in config[pageStyle]:
				col += '{} {},'.format(key,config[pageStyle][key])
			col = col.rstrip(',')
			return "CREATE TABLE if not exists {}_{} ({}) ENGINE = InnoDB DEFAULT CHARSET = utf8 COLLATE = utf8_unicode_ci;".format(self.table_pre,pageStyle,col)
		else:
			return None

	def sql_history(self,rid,pageStyle,run_info,n_record):
		return "insert into {} (rid,page_style,run_info,n_record) values('{}','{}','{}',{})".format(self.table['history'],rid,pageStyle,run_info,n_record)

	def _sql_friendList(self,record,rid):
		if record == {}:
			return []
		pageStyle='friendList'
		if pageStyle not in self.table:
			self._init_table(pageStyle)
		if 'name' not in self.table:
			self._init_table('name')
		val_relation="'),('{}','".format(rid).join(record.keys())
		sql_relation="insert into {} (renrenId1,renrenId2) values ('{}','{}')".format(self.table[pageStyle],rid,val_relation)
		val_name=str(set(record.items())).strip('{}')
		sql_name='insert into {} (renrenId1,name) values {}'.format(self.table['name'],val_name)
		return [sql_relation,sql_name]

	def _sql_status(self,record,rid=None):
		pageStyle='status'
		if record == {}:
			return []
		if pageStyle not in self.table:
			self._init_table(pageStyle)
		sqls=[]
		for statusId,stat in record.items():
			val_stat="statusId='{}'".format(statusId)
			for tag,value in stat.items():
				if value is not None:
					value=value.replace("\\","\\\\").replace("'","\\'").rstrip('\\')#format ' and \ 
				val_stat += ",{}='{}'".format(tag,value)
			sqls.append("insert into {} set {}".format(self.table[pageStyle],val_stat))
		return sqls

	def count(self,n,pageStyle):
		if pageStyle == 'friendList':
			return int(n/2)
		elif pageStyle == 'status':
			return n
		else:
			return -1
