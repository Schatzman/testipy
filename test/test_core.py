#!/usr/bin/env python3.4


import sys
import re
if sys.platform == 'win32':
    sys.path.append('..\\')
elif sys.platform == 'darwin':
    sys.path.append('../')
else:
    print("Hmmm.... unknown platform. What is %s?" % sys.platform)
from testipy import DBHelper
import traceback
import unittest
from util.db import *

class TestipyDBTests(unittest.TestCase):

    def setUp(self):
        self.db_name = 'test.db'
        create_db(self.db_name)
        self.dbh = DBHelper(self.db_name)

    def tearDown(self):
        self.dbh.close_con()
        delete_db(self.db_name)

    # def test_open_con(self):
    #     pass

    # def test_close_con(self):
    #     pass

    # def test_cursor(self):
    #     pass

    def test_db_version(self):
        try:
            self.dbh.close_con()
        except:
            pass
        match = re.search('SQLite Version: \d.\d.\d.\d', self.dbh.db_version())
        if match:
            print(self.dbh.db_version())
        else:
            print(traceback.format_exc())
            raise Exception('No sqlite3 version regex match.')

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestipyDBTests)
    unittest.TextTestRunner(verbosity=2).run(suite)