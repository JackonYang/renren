# -*- coding: utf-8-*-
import urllib
from httplib2 import Http
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

_href_pf_prog = re.compile(r'id=(\d+)">([^<]*?)</a>')
def parser(href_pfs):
    """friendList(['<a href="..?id=1">name1</a>', '<a href="..?id=3">name2</a>']) 
    --> return {id1:name1,id2:name2} if success, return None if error"""
    if href_pfs is None:
        return None
    elif isinstance(href_pfs, str):
        href_pfs = [href_pfs]

    name=dict()
    for href_pf in href_pfs:
        m = _href_pf_prog.search(href_pf)
        if m is None:
            return None
        name[m.group(1)] = m.group(2)
    return name

class renren:
    def __init__(self, user, password):
        self.h = Http()
        self.cookie = self.signin(user, password)

    def signin(self, user, password):
        """sigin to renren.com. return cookie if success."""
        # url
        url = 'http://www.renren.com/PLogin.do'
        home = 'http://www.renren.com/home'
        # headers
        headers = headers_templates.copy()
        # body
        login_data = {
            'email': user,
            'password': password,
            'origURL': home,
            'domain': 'renren.com'
        }
        body = urllib.urlencode(login_data)

        rsp, content = self.h.request(url, 'POST', headers=headers, body=body)
        if '302' == rsp['status']:  # login success
            cookie = rsp['set-cookie']
            print "login success"
            print cookie
        else:
            cookie = None
            print "login error"
        with open('signin_failed_{}.html'.format(user), 'w') as f:
            f.write(content)
        return None

    def friendList(self, rid, maxPages=100):
        urlPtn = "http://friend.renren.com/GetFriendList.do?curpage={}&id=" + rid
        itemPtn = re.compile(r'<div class="info">.*?</div>', re.DOTALL)
        return self.requestIter(urlPtn, itemPtn, maxPages, nResend)

    def renrenId(self):
        proj = re.compile(r'\Wid=(\d+);')
        m = proj.search(self.cookie)
        if m is not None:
            return m.group(1)
        else:
            return None

    def request(self, url, method='GET'):
        """request a page and return html content"""
        headers = headers_templates.copy()
        headers['Cookie'] = self.cookie
        rsp, content = self.h.request(url, method, headers=headers)
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
                    break
            else:
                failedSeq.append(page)
                if len(failedSeq) > maxFailed:
                    return None

        # deal with timeout_seq
        if failedSeq:
            if resend < 0:
                return None
            itemsMore = self.requestIter(urlPtn, itemPtn, failedSeq, resend - 1)
            if itemsMore is None:
                return None
            itemsTotal.update(itemsMore)
        #_safety page check, if itemsAll empty.
        #if (len(itemsAll) ==0) and self._is_safety_page(html_content):
        #        return None, 'account forbidden by safety policy'
        return itemsTotal

if __name__ == '__main__':
    user = raw_input('user(email): ')
    password = raw_input('password: ')
    rr = renren(user, password)
    print rr.cookie
    print rr.renrenId()
    for key, value in parser(rr.friendList(rr.renrenId())):
        print '%s-%s' % (key, value)
