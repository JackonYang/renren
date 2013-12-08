# -*- Encoding: utf-8 -*-
"""
下载并在本地保存人人网数据。

初步解析的数据和 Cookie 均保存在本地 Cache 目录下。
"""
# TODO:
# Cookie
#   1. request 时，如果 cookie 为空，可以自动加载 cookie 或退出
#   2. signin 时，在本地保存 cookie
# local save
#   3. requestIter 时，本地保存初步解析的数据
# statistics
#   4. 保存 requestIter 的性能信息，mean/max/min
import urllib
from httplib2 import Http
import os
import re
import klog.logger as klogger
from login.renren import login, parseRenrenId

maxFailed = 5
nResend = 3
headers_templates = {
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/534.24 (KHTML, like Gecko) Chrome/11.0.696.65 Safari/534.24',
    'Content-type': 'application/x-www-form-urlencoded',
    'Accept': '*/*',
    'Accept-Charset': 'UTF-8,*;q=0.5',
    'Accept-Encoding': 'gzip,deflate,sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Cache-Control': 'no-cache',
}

log = klogger.debugLog()


class renren:
    def __init__(self, user, password):
        self.h = Http()
        self.headers = headers_templates.copy()
        self.headers['Cookie'] = login(user, password)

    def renrenId(self):
        return parseRenrenId(self.headers['Cookie'])

    def friendList(self, rid, maxPages=100):
        urlPtn = "http://friend.renren.com/GetFriendList.do?curpage={}&id=" + rid
        itemPtn = re.compile(r'<div class="info">.*?</div>', re.DOTALL)
        log.info('request {} of {}'.format('friendList', rid))
        return self.requestIter(urlPtn, itemPtn, maxPages, nResend)

    def status(self, rid, maxPages=100):
        urlPtn = "http://status.renren.com/status?curpage={}&id=" + rid + "&__view=async-html"
        itemPtn = re.compile(r'<li data-wiki\W* id="status-\d+">.*?</li>', re.DOTALL)
        log.info('request {} of {}'.format('status', rid))
        return self.requestIter(urlPtn, itemPtn, maxPages, nResend)

    def request(self, url, method='GET'):
        """request a page and return html content"""
        rsp, content = self.h.request(url, method, headers=headers)
        # with open('fl.html', 'w') as f:
        #    f.write(content)
        return content

    def requestIter(self, urlPtn, itemPtn, pageRange, resend):
        """__iter_page(urlPtn, itemPtn, pageRange, resend) --> items:set()"""
        if isinstance(pageRange, int):
            pageRange = range(pageRange)

        itemsTotal = set()
        failedSeq = list()

        # request next page until no more items detected
        for page in pageRange:
            content = self.request(urlPtn.format(page))
            if content is not None:
                itemsPage = itemPtn.findall(content)
                if itemsPage:
                    itemsTotal.update(itemsPage)
                else:  # privacy, all pages requested, or safety page
                    log.debug('nothing contains in page/renrenId {}/{})'.format(page, self.renrenId()))
                    break
            else:
                log.warn('request page/renrenId {}/{} failed'.format(page, self.renrenId()))
                failedSeq.append(page)
                if len(failedSeq) > maxFailed:
                    log.error('more timeout than {}'.format(maxFailed))
                    return None

        # deal with timeout_seq
        if failedSeq:
            if resend < 0:
                return None
            log.debug('resend failed pages: {}'.format(failedSeq))
            itemsMore = self.requestIter(urlPtn, itemPtn, failedSeq, resend - 1)
            if itemsMore is None:
                return None
            itemsTotal.update(itemsMore)
        #_safety page check, if itemsAll empty.
        #if (len(itemsAll) ==0) and self._is_safety_page(html_content):
        #        return None, 'account forbidden by safety policy'
        return itemsTotal


if __name__ == '__main__':
    from settings import account
    rr = renren(account['email'], account['password'])
    print rr.renrenId()
    # print len(rr.friendList(rr.renrenId()))
