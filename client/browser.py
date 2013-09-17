# -*- Encoding: utf-8 -*-
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


class renren:
    def __init__(self, user, password, autoLogin=True):
        self.h = Http()
        self.cookieFile = 'renren_{}.cookie'.format(user)
        self.cookie = self.__get_cookie()
        if autoLogin and (self.cookie is None):  # check cookie validate
            self.cookie = self.signin(user, password)
            # print 'login'
        else:
            pass
            # print 'no need login'

    def signin(self, user, password):
        """sigin to renren.com. return and save cookie if success."""
        # TODO:
        # 1. deal with timeout
        # 2. random useragent
        # 3. more accurate headers
        # 5. deal with verfication code and passwd error

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
            # print 'login success'
            cookie = rsp['set-cookie']
            self.__save_cookie(cookie)
            return cookie
        else:
            with open('signin_failed_{}.html'.format(user), 'w') as f:
                f.write(content)
            return None

    def friendList(self, rid, maxPages=100):
        urlPtn = "http://friend.renren.com/GetFriendList.do?curpage={}&id=" + rid
        itemPtn = re.compile(r'<dd>\s*<a\s+href="http://www.renren.com/profile.do\?id=\d+">.*?</a>')
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
        #with open('fl.html', 'w') as f:
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
                    break
            else:
                failedSeq.append(page)
                # break when much more timeout than normal
                if len(failedSeq) > maxFailed:
                    return None  # 'more timeout than maxFailed'

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

    def __get_cookie(self):
        cookie = None
        if os.path.exists(self.cookieFile):
            with open(self.cookieFile, 'r') as f:
                cookie = f.read().strip(' \n')
        return cookie

    def __save_cookie(self, cookie):
        with open(self.cookieFile, 'w') as f:
            f.write(cookie)


if __name__ == '__main__':
    from settings import account
    rr = renren(account['email'], account['password'])
    print len(rr.friendList(rr.renrenId()))
