# -*- Encoding: utf-8 -*-
import urllib
from httplib2 import Http
import os

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
        self.cookie = self.__get_cookie(user, 'renren')
        if autoLogin and (self.cookie is None):  # check cookie validate
            self.cookie = self.signin(user, password)
            # print 'login'
        else:
            pass
            # print 'no need login'

    def signin(self, user, password):
        """sigin to renren.com. return cookie if success."""
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
            self.__save_cookie(cookie, user, 'renren')
            return cookie
        else:
            with open('signin_failed_{}.html'.format(user), 'w') as f:
                f.write(content)
            return None

    def request(self, url, method='GET'):
        return self.h.request(url, method, headers=self.headers)

    def __get_cookie(self, user, website='renren'):
        filename = '{}_{}.cookie'.format(website, user)
        cookie = None
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                cookie = f.read().strip(' \n')
        return cookie

    def __save_cookie(self, cookie, user, website='renren'):
        filename = '{}_{}.cookie'.format(website, user)
        with open(filename, 'w') as f:
            f.write(cookie)


if __name__ == '__main__':
    from settings import account
    renren(account['email'], account['password'])
    #url = "http://friend.renren.com/GetFriendList.do?curpage={}&id={}".format(0, rr.renrenId)
    #print url
    #rsp, content = rr.request(url)
    #print rsp
    #with open('friendlist.html', 'w') as f:
    #    f.write(content)
