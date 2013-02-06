renren
======

人人网信息抓取与社交信息挖掘

单线程后台运行。

spider
  |--download
  |    |--parse
  |
  |--database

spider 直接依赖于 download 和 database 两个 class。

download 为每一个页面类型(pageStyle)提供一个下载接口:
pageStyle(renrenId)-->(items,timecost,pageStyle)

database 为每一个页面类型提供一个存储接口：
pageStyle(item,renrenId=None) --> nItemsSave

download 获取页面，并调用 parse module 中封装的方法解析出 items 。
