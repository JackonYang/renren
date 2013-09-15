import unittest
from browser import cookies


class test_cookies(unittest.TestCase):
    def setUp(self):
        self.filename = 'test_cookie.p'
        del_if_exists(self.filename)

    def tearDown(self):
        del_if_exists(self.filename)
        self.filename = None

    def test_load_save(self):
        ck = cookies(self.filename)
        self.assertEquals(ck.cookie, {})

        user = 'user1'
        website = 'renren'
        cookie = 'cookie1'

        ck.add(user, website, cookie)
        self.assertEquals(ck.cookie, {(user, website): cookie})

        ck.add(user, website, cookie)
        self.assertEquals(ck.cookie, {(user, website): cookie})

        ck = None

        ck2 = cookies(self.filename)
        self.assertEquals(ck2.cookie, {(user, website): cookie})


def del_if_exists(filename):
    import os
    if os.path.exists(filename):
        os.remove(filename)


def testSet(suite):
    suite.addTest(test_cookies('test_load_save'))

if __name__ == '__main__':
    suite = unittest.TestSuite()
    testSet(suite)
    runner = unittest.TextTestRunner()
    runner.run(suite)
