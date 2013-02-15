design of renrenSpider
====================

抓取并在本地存储社交网络数据，数据源：[www.renren.com](www.renren.com)

renren spider 直接依赖于 browser 和 repo。repo 可以选择 database, file etc

* browser:抓取页面并返回 record 和 运行信息（timecost or error info)。<br>
* repo: 本地保存 record 和 download history，提供读写接口。

USAGE
-----

#### 用法: 

- 运行命令 `python3 getMyNet2.py` 来抓取：

	1. 自己的二级网络结构，即：自己的好友列表、好友的好友列表。
	2. 自己的人人网状态、好友的人人网状态。

- 运行命令 `python3 get_my_net3_status.py ` 抓取 3 级网络的状态。
- 运行命令 `python3 get_my_net3_friendList.py` 抓取 3 级网络结构。

默认 info 级日志，记录各 renren id 的抓取细节（下载和保存的record数，抓取耗时）。
日志输出在当前目录的  run.log 文件中。

#### 环境要求：

* ubuntu/windows
* python3.2
* mysql
* pymysql: [install package link](https://github.com/petehunt/PyMySQL)


#### 参数配置：

1. 在 `getMyNetxxx.py` 文件开始处配置 人人网的登录帐号和密码。
2. 在 `db_renren.ini` 中配置数据库信息，通常只需修改 `host`,`user`,`passwd`

INTERFACE
---------

#### browse 
* `pageStyle(renrenId) --> (record:dict,timecost:str)` 下载 pageStyle 页面的信息字段。
* `login(user,passwd) --> (renrenId,info)` 社交网站登录

#### repo-database
* `save_pageStyle(record,rid,run_info) --> nItemSave` 保存 record 和 history
* `getSearched(pageStyle) --> rids:set`
* `getFriendList(rid) --> friendsId:set`

#### spider
* `login() --> same as browser.login()` login [www.renren.com](www.renren.com)
* `getStatus_friend(rid) --> None` get status of rid's friends
* `getNet2(rid) --> None` get friendList of rid's friends

design of class
--------------------

####  browser：

1. `_download`<br>
简单的根据 url 获取 `html_content` 并返回给上层调用，便于性能统计。

2. `_iter_page`<br>
页面类型分为：迭代的多页面，如 friendList, status; 单页面，如 profile,homepage。<br>
实际抓取以迭代页面为主，对方出于性能考虑，通常鉴权较少，安全策略低。<br>
`_iter_page` 迭代调用`_download`获取`html_content`并识别出其中的 items。

3. parse <br>
解析 `_iter_page` 得到的 items, 获得信息字段 record。返回 dict()。<br>
迭代页面一般包含多个 item，每个 item 有自己的 id。以此作为 dict 的 key。<br>
单页面一般包含多个字段，可以处理为 tag = value 格式。以此作为 dict 的 key 和 value。

**内部接口规范**

1. `_download(url:str) --> html_content:str`
2. `_iter_page(pageStyle,rid)  --> (items:set,'success'/error_info:str)` info is success or error info
3. `parse.pageStyle(items:set) --> record:dict() `

_parse.pageStyle 每次只解析一个用户特定 pageStyle 的字段_

####  repo-mysql：

以 mysql 作为本地存储介质。

每一类 `pageStyle` 一个接口，若传递了 `run_info` 字段，则自动写 `history`

1. `save_pageStyle` 存储 record 和 history
3. `self.table` 内部属性，已经确认创建的表空间及表名。
4. `_init_table` 根据 pageStyle 创建表空间并初始化 `self.table`
5. `_getConn` 获取 mysql conn。数据库连接参数在 `db_renren.ini` 中配置。
2. `getSearched` 查询 history 表，获取已查询集合。
3. `get_friendList`

**内部接口规范**

1. `save_pageStyle(record:dict, rid:str) --> number_of_items_saved:int` call `_save_process` to save record and history
2. `_save_process(pageStyle:str, record:dict, rid:str, run_info:str) --> number_of_items_saved:int`
3. `_sql_pageStyle(record:dict,rid:str) --> sqls:list` called by `_save_process` to construct sqls
4. `_sql_create_table(pageStyle:str) --> sql` call by `_init_table`, read table info from config file and return sql for create table.

#### profile

请求 profile 页面，可能返回 2 种页面，分别包含以下字段。

1. profile detail.

	- basic: birthday, hometown, gender
	- edu: college, senior, junior, primary, technology
	- work: company, period
	- contact: empty and no use. qq, msn,phone, domains, personal website
2. profile brief.

	- basic: gender, birthday, hometown
	- present: location/address, work, school

#### spider

各种功能方法中生成待抓取的 `rid` 序列，由 `seq_process` 抓取。

#### 内部接口规范
1. `seq_process(toSearch:str/set,pageStyle:str)` download and save record
