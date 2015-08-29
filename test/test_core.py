#!/usr/bin/env python3.4

import unittest
import sys
if sys.platform == 'win32':
    sys.path.append('..\\')
elif sys.platform == 'darwin':
    sys.path.append('../')
else:
    print("Hmmm.... unknown platform. What is %s?" % sys.platform)
from testipy import DBHelper
from util.db import *

class TestipyDBTests(unittest.TestCase):

    def setUp(self):
        self.db_name = 'test.db'
        create_db(self.db_name)
        self.dbh = DBHelper(self.db_name)

    def tearDown(self):
        delete_db(self.db_name)

    def test_open_con(self):
        pass

    def test_close_con(self):
        pass

    def test_cursor(self):
        pass

    def test_db_version(self):
        print(self.dbh.db_version())
        import pdb; pdb.set_trace()

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestipyDBTests)
    unittest.TextTestRunner(verbosity=2).run(suite)