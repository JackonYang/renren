# -*- Encoding: utf-8 -*-
import urllib
from httplib2 import Http
import os
import re

max_timeout = 5
resend_n = 3
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

    def friendList(self, rid, max_pages=100):
        url_ptn = "http://friend.renren.com/GetFriendList.do?curpage={}&id={}"
        item_ptn = re.compile(r'<dd>\s*<a\s+href="http://www.renren.com/profile.do\?id=\d+">.*?</a>')
        return self.__iter_page(url_ptn, item_ptn, rid, max_pages, resend_n)

    def renrenId(self):
        import re
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
        with open('fl.html', 'w') as f:
            f.write(content)
        return content

    def __iter_page(self, url_ptn, item_ptn, rid, pages, resend):
        """__iter_page(pageStyle, rid) --> items:set()"""
        if resend < 0:
            return None
        if isinstance(pages, int):
            pages = range(pages)

        itemsAll = set()
        timeout_seq = list()

        # request next page until no more items detected
        for curpage in pages:
            try:
                html_content = self.request(url_ptn.format(curpage, rid))
            except:
                timeout_seq.append(curpage)
                # break when much more timeout than normal
                if len(timeout_seq) > max_timeout:
                    return None  # 'more timeout than max_timeout'
            else:
                items_curpage = item_ptn.findall(html_content)  # detect items
                if len(items_curpage) > 0:
                    itemsAll.update(items_curpage)
                else:  # privacy, all pages requested, or safety page
                    break
        # deal with timeout_seq
        if timeout_seq:  # resend
            item_re = self.__iter_page(url_ptn, item_ptn, rid, timeout_seq, resend - 1)
            if item_re is None:
                return None
            else:
                itemsAll.update(item_re)
        #_safety page check, if itemsAll empty.
        #if (len(itemsAll) ==0) and self._is_safety_page(html_content):
        #        return None, 'account forbidden by safety policy'
        return itemsAll

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
