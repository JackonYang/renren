# -*- Encoding: utf-8 -*-
"""
下载并在本地保存人人网数据。
"""
from httplib2 import Http
import os
import re

from login.renren import parseRenrenId

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
    def __init__(self, user, password=None):
        self.h = Http()
        # self.headers = headers_templates.copy()
        self.headers = headers_templates.copy()
        if False: #user.lower() == 'cookie':
            self.headers['Cookie'] = raw_input('Please input cookie(document.cookie): ')
        else:
            #password = raw_input('Please input your password: ')
            self.headers['Cookie'] = "anonymid=hydr1qdn-ycm6wf; _r01_=1; JSESSIONID=abcKEdr0RzVXX9ifHSzEu; XNESSESSIONID=abcuFh17apWB-7i2oLfFu; depovince=GW; jebecookies=4732ccf8-d2ea-49cc-ad1c-69c8c9cd00be|||||; ick_login=d972250b-250e-4ece-9679-2c064a6763a6; _de=BA3DF646D479464C7CEAE61F3CB0A4C15212E40F3D18115C; p=3dc4a0e170c839b1003c15e0645561b28; ap=539841008; ln_uact=xucengg65243@163.com; ln_hurl=http://hdn.xnimg.cn/photos/hdn321/20140302/2335/h_main_zS6y_227600004407113e.jpg; t=cb5ac4601a607a3f85b1264373f5a76b8; societyguester=cb5ac4601a607a3f85b1264373f5a76b8; id=539841008; xnsid=ec249437; loginfrom=null; feedType=539841008_hot; jebe_key=d608be53-46cd-46e1-956f-9d676d9e907f%7C6fad6b404f16365a47e2b1e47fd7a30d%7C1413377389697%7C1%7C1413377389844; l4pager=1"
            # login in

    def renrenId(self):
        return parseRenrenId(self.headers['Cookie'])

    def request(self, url, method='GET'):
        """request a page and return html content"""
        rsp, content = self.h.request(url, method, headers=self.headers)
        return content

    def friendList(self, rid, maxPages=200):
        urlPtn = "http://friend.renren.com/GetFriendList.do?curpage={}&id=" + rid
        itemPtn = re.compile(r'<a href="http://www.renren.com/profile.do\?id=(\d+)">([^<]*)</a>', re.DOTALL)
        print('\nstart to request {} of {}'.format('friendList', rid))
        resend = nResend
        pageRange = range(maxPages)
        itemsTotal = set()
        failedSeq = list()

        # request next page until no more items detected
        for page in pageRange:
            content = self.request(urlPtn.format(page))
            if content is not None:
                itemsPage = itemPtn.findall(content)
                if itemsPage and len(itemsPage) > 1:
                    print('{} items in page/renrenId {}/{})'.format(len(itemsPage)-1, page, self.renrenId()))
                    itemsTotal.update(itemsPage)
                else:  # privacy, all pages requested, or safety page
                    print('nothing contains in page/renrenId {}/{})'.format(page, self.renrenId()))
                    break
            else:
                print('request page/renrenId {}/{} failed. re-request later'.format(page, self.renrenId()))
                failedSeq.append(page)
                if len(failedSeq) > maxFailed:
                    print('more timeout than {}'.format(maxFailed))
                    return None

        # deal with timeout_seq
        if failedSeq:
            if resend < 0:
                return None
            print('resend failed pages: {}'.format(failedSeq))
            itemsMore = self.requestIter(urlPtn, itemPtn, failedSeq, resend - 1)
            if itemsMore is None:
                return None
            itemsTotal.update(itemsMore)
        filename = 'friendlist_%s.txt' % rid
        print('\nDone! {} friends got. saved in {}'.format(len(itemsTotal)-1, filename))
        with open(filename, 'w') as f:
            f.write(','.join(["@%s(%s)" % one_data for one_data in itemsTotal]))


if __name__ == '__main__':
    email = '0' # raw_input('Please input your email(type `cookie` to login by cookie): ')
    rr = renren(email)
    rr.friendList(rr.renrenId())
