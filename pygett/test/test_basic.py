import unittest
import sys, os
import re

#: Make sure our code is importable from this relative path
sys.path.insert(0, os.path.abspath('../..'))

from pygett import Gett
from pygett.shares import GettShare
from pygett.files import GettFile

login_params = {
    "apikey": "apitest",
    "email": "apitest@ge.tt",
    "password": "secret"
}

class BasicGettTests(unittest.TestCase):

    def setUp(self):
        self.client = Gett(**login_params)
        self.share = self.client.get_share("928PBdA")
        self.f = self.client.get_file("928PBdA", 0)

    def tests(self):
        self.assertEqual(type(self.client), type(Gett(apikey="a", email="B@b", password="c")))
        self.assertEqual(type(self.share), type(GettShare({})))
        self.assertEqual(type(self.f), type(GettFile({})))
        self.assertEqual(self.share.sharename, "928PBdA")
        self.assertEqual(self.share.created, 1322847473)
        self.assertTrue(re.search(r"Test", self.share.title))
        self.assertEqual(len(self.share.files), 2)
        self.assertEqual(self.f.filename, "hello.c")
        self.assertEqual(self.f.fileid, '0')
        self.assertEqual(self.f.created, 1322847473)
        contents = self.f.contents()
        self.assertEqual(self.f.size, len(contents))
        self.assertTrue(re.search(r"Hello world", contents))

if __name__ == '__main__':
    unittest.main()
