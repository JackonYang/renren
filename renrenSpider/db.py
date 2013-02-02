import pymysql

class rDb:
	sqls=dict()
	sqls['name']='CREATE TABLE if not exists {} (renrenId1 varchar(15) NOT NULL,name varchar(20),lastmodified TIMESTAMP DEFAULT NOW() {})ENGINE=InnoDB DEFAULT CHARSET = utf8 COLLATE = utf8_unicode_ci;'
	sqls['relation']='CREATE TABLE if not exists {} (renrenId1 varchar(15) NOT NULL,renrenId2 varchar(15) NOT NULL,KEY one(renrenId1),KEY two(renrenId2),lastmodified TIMESTAMP DEFAULT NOW() {} )ENGINE = InnoDB DEFAULT CHARSET = utf8 COLLATE = utf8_unicode_ci;'
	key={'name':',KEY idx_temp(renrenId1)','relation':',KEY idx_temp (renrenId1,renrenId2)','profile':',KEY (renrenId1)'}
	primary={'name':',PRIMARY KEY (renrenId1)','profile':',PRIMARY KEY (renrenId1)','relation':',PRIMARY KEY (renrenId1,renrenId2)'}

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

	def insertFriendList(self,renrenId,names):
		if names is None:
			return -1
		elif names is dict():
			names={'0':'null'}
			
		valFl='),({},'.format(renrenId).join(names.keys())
		sqlFl='insert into {} (renrenId1,renrenId2) values ({},{})'.format(self.tempTable['relation'],renrenId,valFl)
		valNm=str(set(names.items())).strip('{}')
		sqlNm='insert into {} (renrenId1,name) values {}'.format(self.tempTable['name'],valNm)
		try:
			self.cur.execute(sqlFl)
			self.cur.execute(sqlNm)
		except Exception as e:
			print(sqlFl)
			print(sqlNm)
		else:
			self.conn.commit()

	def getRenrenId(self,col,renrenId):
		target=str(col)
		where=str(col%2+1)
		res=set()
		for table in [self.mainTable['relation'],self.tempTable['relation']]:
			self.cur.execute("SELECT renrenId{} FROM {} where renrenId{}={}".format(target,table,where,renrenId))
			for item in self.cur.fetchall():
				res.add(item[0])
		return res
	def getSearched(self,info):
		res=set()
		for table in [self.mainTable[info],self.tempTable[info]]:
			self.cur.execute("SELECT renrenId1 FROM {} group by renrenId1".format(table))
			for item in self.cur.fetchall():
				res.add(item[0])
		return res

	def createTempTable(self):
		for attr in self.sqls.keys():
			self.cur.execute(self.sqls[attr].format(self.tempTable[attr],self.key[attr]))
	def createMainTable(self):
		for attr in self.sqls.keys():
			self.cur.execute(self.sqls[attr].format(self.mainTable[attr],self.primary[attr]))
	def dropTempTable(self):
		for table in self.tempTable.values():
			self.cur.execute('drop table if exists {}'.format(table))
