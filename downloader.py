# -*- Encoding: utf-8 -*-
"""
下载并在本地保存人人网数据。
"""
from httplib2 import Http
import logging
import os
import re

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

class renren:
    def __init__(self, cookie):
        self.h = Http()
        self.headers = headers_templates.copy()
        self.headers['Cookie'] = cookie

        self.m_log = logging.getLogger('renren.downloader')
        self.m_log.setLevel(logging.WARNING)
        log_dir = 'log'
        if not os.path.exists(log_dir):
            os.mkdir(log_dir)
        logfile = os.path.join(log_dir, 'download.log')
        hdlr = logging.FileHandler(logfile)
        hdlr.setFormatter(logging.Formatter('%(asctime)s|%(levelname)s|%(message)s|%(filename)s-%(lineno)s'))
        self.m_log.addHandler(hdlr)

    def renrenId(self):
        proj = re.compile(r'\Wid=(\d+);')
        m = proj.search(self.headers['Cookie'])
        if m is not None:
            return m.group(1)
        else:
            return None

    def friendList(self, rid, maxPages=100):
        urlPtn = "http://friend.renren.com/GetFriendList.do?curpage={}&id=" + rid
        itemPtn = re.compile(r'<a href="http://www.renren.com/profile.do\?id=(\d+)">([^<]*)</a>', re.DOTALL)
        self.m_log.info('request {} of {}'.format('friendList', rid))
        return self.requestIter(urlPtn, itemPtn, maxPages, nResend)

    def status(self, rid, maxPages=100):
        urlPtn = "http://status.renren.com/status?curpage={}&id=" + rid + "&__view=async-html"
        itemPtn = re.compile(r'<li data-wiki\W* id="status-\d+">.*?</li>', re.DOTALL)
        self.m_log.info('request {} of {}'.format('status', rid))
        return self.requestIter(urlPtn, itemPtn, maxPages, nResend)

    def request(self, url, method='GET'):
        """request a page and return html content"""
        rsp, content = self.h.request(url, method, headers=self.headers)
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
                if itemsPage and len(itemsPage) > 1:
                    itemsTotal.update(itemsPage)
                else:  # privacy, all pages requested, or safety page
                    self.m_log.debug('nothing contains in page/renrenId {}/{})'.format(page, self.renrenId()))
                    break
            else:
                self.m_log.warn('request page/renrenId {}/{} failed'.format(page, self.renrenId()))
                failedSeq.append(page)
                if len(failedSeq) > maxFailed:
                    self.m_log.error('more timeout than {}'.format(maxFailed))
                    return None

        # deal with timeout_seq
        if failedSeq:
            if resend < 0:
                return None
            self.m_log.debug('resend failed pages: {}'.format(failedSeq))
            itemsMore = self.requestIter(urlPtn, itemPtn, failedSeq, resend-1)
            if itemsMore is None:
                return None  # return None if not in its integrity
            itemsTotal.update(itemsMore)
        #_safety page check, if itemsAll empty.
        #if (len(itemsAll) ==0) and self._is_safety_page(html_content):
        #        return None, 'account forbidden by safety policy'
        return itemsTotal


if __name__ == '__main__':
    test_cookie = raw_input('Input cookie(document.cookie): ')
    rr = renren(test_cookie)
    print rr.renrenId()
    print len(rr.friendList(rr.renrenId()))
