design of renrenSpider
====================

抓取并在本地存储社交网络数据，数据源：[www.renren.com](www.renren.com)

core framework
---------------------

renren spider 直接依赖于 browser 和 database 两个类。<br>
前者负责抓取页面并解析出信息字段 record。database 封装数据库读写操作。

download 为每一个页面类型 (pageStyle) 提供一个下载接口:<br>
`pageStyle(renrenId)-->(items,timecost,pageStyle)`

database 为每一个页面类型提供一个存储接口：<br>
`pageStyle(item,renrenId=None) --> nItemsSave`


####  browser 核心实现：

1. `_download`<br>
简单的根据 url 获取 `html_content` 并返回给上层调用，便于性能统计。

2. `_iter_page`<br>
页面类型分为可以迭代的多页面，如 friendList, status; 单页面，如 profile,homepage。<br>
实际抓取以迭代页面为主，对方出于性能考虑，通常鉴权较少，安全策略低。<br>
`_iter_page` 迭代调用`_download`获取`html_content`并识别出其中的 items。

3. parse <br>
解析 detect 得到的 items, 获得信息字段 record。返回 dict()。<br>
迭代页面包含多个 item，通常，每个item会有自己的id。以此作为 dict 的 key。<br>
单页面一般包含多个字段，可以处理为 tag=value 格式。以此作为 dict 的 key 和 value。

####  database 核心实现：

1. `save_pageStyle`
2. `getSearched_pageStyle`
3. `getRecord`

#### 接口规范 

1. `download(url:str) --> html_content:str`
1. `_iter_page(pageStyle,rid)  --> (items:set)`
2. `parse.pageStyle(items:set) --> record:dict() `
3. `browser.pageStyle(rid:str) --> (record:dict(),timecost:str)`
3. `database.save(rid:str,record) --> number_of_items_saved:int`

_parse.pageStyle 每次只解析一个用户特定 pageStyle 的字段_
