# -*- Encoding: utf-8 -*-
import urllib
from httplib2 import Http


class renren:
    def __init__(self, autoLogin=True):
        self.h = Http()
        self.headers = {
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/534.24 (KHTML, like Gecko) Chrome/11.0.696.65 Safari/534.24',
            'Content-type': 'application/x-www-form-urlencoded',
            'Accept': '*/*',
            'Accept-Charset': 'UTF-8,*;q=0.5',
            'Accept-Encoding': 'gzip,deflate,sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Cache-Control': 'no-cache',
        }
        self.renrenId = None
        if autoLogin and (self.renrenId is None):
            # print 'begin login'
            self.signin()

    def signin(self):
        # url
        url = 'http://www.renren.com/PLogin.do'
        home = 'http://www.renren.com/home'
        # body
        from settings import account
        login_data = {
            'origURL': home,
            'domain': 'renren.com'
        }
        login_data.update(account)
        body = urllib.urlencode(login_data)

        rsp, content = self.h.request(url, 'POST', headers=self.headers, body=body)
        if '302' == rsp['status']:  # login success
            # print 'login success'
            self.headers['Cookie'] = rsp['set-cookie']
            rsp, content = self.h.request(home, "GET", headers=self.headers)
            import re
            m = re.compile(r'http://www.renren.com/(\d+)').match(rsp['content-location'])
            if m is not None:
                self.renrenId = m.group(1)
        else:
            print rsp['status']
            with open('home_error.html', 'w') as f:
                f.write(content)

    def request(self, url, method='GET'):
        return self.h.request(url, method, headers=self.headers)


if __name__ == '__main__':
    rr = renren()
    print rr.renrenId
    url = "http://friend.renren.com/GetFriendList.do?curpage={}&id={}".format(0, rr.renrenId)
    print url
    rsp, content = rr.request(url)
    print rsp
    with open('friendlist.html', 'w') as f:
        f.write(content)
