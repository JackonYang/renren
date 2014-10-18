import MySQLdb
from settings import db_connet_info as connect_info


def _sql_log_fl(rid, login_id, n_record):
    return "INSERT INTO stat_log_friends (rid, login_id, n_record) VALUES ('%s', '%s', %d)" % (rid, login_id, n_record)

def _sql_fl(record, rid):
    val_fl = ','.join(["('%s', '%s')" % (rid, item[0]) for item in record if item[0] != rid])
    return "INSERT INTO friends (rid1, rid2) VALUES %s" % val_fl

def _sql_name(record):
        val_name = ','.join(["('%s', '%s')" % item for item in record])
        return "INSERT INTO profile (rid, name) VALUES %s" % val_name

class repo_mysql:

    def __init__(self):
        self.conn = MySQLdb.connect(**connect_info)
        self.cur = self.conn.cursor()

    def __del__(self):
        self.cur.close()
        self.conn.close()

    def save_fl(self, login_id, rid, fl_record):
        """save record and return rows affected.save nothing if empty.
        return None if input error"""
        n_fl = self.cur.execute(_sql_fl(fl_record, rid))
        n_name = self.cur.execute(_sql_name(fl_record))
        self.cur.execute(_sql_log_fl(rid, login_id, len(fl_record)))
        self.conn.commit()
        return n_fl

    def get_fl_searched(self):
        self.cur.execute("SELECT rid FROM stat_log_friends")
        return {item[0] for item in self.cur.fetchall()}

    def get_fl(self, rid):
        self.cur.execute("SELECT rid2 FROM friends where rid1='%s'" % rid)
        return {item[0] for item in self.cur.fetchall()}

    def _sql_status(self,record,rid=None):
        pageStyle='status'
        if record == {}:
            return []
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

    def tag_exceed(self,rid,k,v):
        print('pf tag exceed. tag={},renrenId={},value={}'.format(k,rid,v))

if __name__ == '__main__':
    from downloader import renren
    test_cookie = raw_input('Input cookie(document.cookie): ')
    rr = renren(test_cookie)
    rid = rr.renrenId()
    print rid
    record = rr.friendList(rr.renrenId())
    print '%d got' % len(record)

    repo = repo_mysql()
    print repo.save_fl(rid, rid, record)
    print 'friends of rid: %s' % len(repo.get_fl(rid))
    print 'searched: %s' % ','.join(repo.get_fl_searched())

