import pymysql

cfg_filename='config/mysql.ini'

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

class repo_mysql:
    def __init__(self,table_pre='test'):
        self.table_name={}
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

    def save_profile(self,record,rid,run_info=None):
        """save profile and return rows affected.return None if input error"""
        return self._save_process('profile',record,rid,run_info)

    def _save_process(self,pageStyle,record,rid,run_info):
        """save record and return rows affected.save nothing if empty.
        return None if input error"""
        if not isinstance(record,dict):
            return None
        sql_meth=getattr(self,'_sql_{}'.format(pageStyle))
        sqls=sql_meth(record,rid)
        n=0
        try:
            for sql in sqls:
                n += self.cur.execute(sql)
            if run_info is not None:#write log 
                self.cur.execute(self.sql_history(rid,pageStyle,run_info,len(record)))
            self.conn.commit()
        except Exception as e:
            print(e)
            print(sqls)
        return self.count(n,pageStyle)

    def getSearched(self,pageStyle):
        #only success download is logged
        res=set()
        self.cur.execute("SELECT rid FROM {} where page_style='{}'".format(self.table_name['history'],pageStyle))
        for item in self.cur.fetchall():
            res.add(item[0])
        return res

    def getFriendList(self,renrenId):
        return self._getRenrenId(2,renrenId)

    def _getRenrenId(self,col,renrenId):
        pageStyle='friendList'
        if pageStyle not in self.table_name:
            self._init_table(pageStyle)
        target=str(col)
        where=str(col%2+1)
        res=set()
        self.cur.execute("SELECT renrenId{} FROM {} where renrenId{}={}".format(target,self.table_name[pageStyle],where,renrenId))
        for item in self.cur.fetchall():
            res.add(item[0])
        return res

    def _init_table(self,table):
        cols=get_cfg_dict(table)
        if cols is None:
            return None
        self.table_name[table]='{}_{}'.format(self.table_pre,table)
        col=",".join(["{} {}".format(k,v) for k, v in cols.items()])
        sql_create="CREATE TABLE if not exists {} ({}) ENGINE = InnoDB DEFAULT CHARSET = utf8 COLLATE = utf8_unicode_ci;"\
                .format(self.table_name[table],col)
        self.cur.execute(sql_create)
        self.conn.commit()

    def _getConn(self):
        connect_info=get_cfg_dict('connect',False)
        key_type={'port':int}
        for key,t in key_type.items():
            if key in connect_info:
                connect_info[key]=t(connect_info[key])
        return pymysql.connect(**connect_info)

    def sql_history(self,rid,pageStyle,run_info,n_record):
        return "insert into {} (rid,page_style,run_info,n_record) values('{}','{}','{}',{})".format(self.table_name['history'],rid,pageStyle,run_info,n_record)

    def _sql_friendList(self,record,rid):
        if len(record) == 0:
            return []
        pageStyle='friendList'
        if pageStyle not in self.table_name:
            self._init_table(pageStyle)
        if 'name' not in self.table_name:
            self._init_table('name')
        val_relation="'),('{}','".format(rid).join(record.keys())
        sql_relation="insert into {} (renrenId1,renrenId2) values ('{}','{}')".format(self.table_name[pageStyle],rid,val_relation)
        val_name=str(set(record.items())).strip('{}')
        sql_name='insert into {} (renrenId1,name) values {}'.format(self.table_name['name'],val_name)
        return [sql_relation,sql_name]

    def _sql_status(self,record,rid=None):
        pageStyle='status'
        if record == {}:
            return []
        if pageStyle not in self.table_name:
            self._init_table(pageStyle)
        sqls=[]
        for statusId,stat in record.items():
            val_stat="statusId='{}'".format(statusId)
            for tag,value in stat.items():
                if value is not None:
                    value=value.replace("\\","\\\\").replace("'","\\'").rstrip('\\')#format ' and \ 
                val_stat += ",{}='{}'".format(tag,value)
            sqls.append("insert into {} set {}".format(self.table_name[pageStyle],val_stat))
        return sqls

    def _sql_profile(self,record,rid=None):
        pageStyle='profile'
        if len(record) == 0:
            return []
        if pageStyle not in self.table_name:
            self._init_table(pageStyle)
        pf_map=get_cfg_dict('profile_map',has_default=False)
        pf_ignore=pf_map.pop('ignore').split(',')
        #construct sql 
        pfs="renrenId1='{}'".format(rid)
        for k,v in record.items():
            if k in pf_map.keys():
                pfs += ",{}='{}'".format(pf_map[k],v)
            elif k in pf_map.values():
                pfs += ",{}='{}'".format(k,v)
            elif k in pf_ignore:
                #print('ignore {}'.format(k))
                pass
            else:
                self.tag_exceed(rid,k,v)
        sql_pf="insert into {} set {}".format(self.table_name[pageStyle],pfs)
        return [sql_pf]

    def count(self,n,pageStyle):
        if pageStyle == 'friendList':
            return int(n/2)
        elif pageStyle == 'status':
            return n
        elif pageStyle == 'profile':
            return n
        else:
            return -1

    def tag_exceed(self,rid,k,v):
        print('pf tag exceed. tag={},renrenId={},value={}'.format(k,rid,v))
