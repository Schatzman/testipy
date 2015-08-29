#!/usr/bin/env python3.4

import unittest
import sys
if sys.platform == 'win32':
    sys.path.append('..\\')
from trol import DBHelper
from util.db import *

class TrolDBTests(unittest.TestCase):

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
        pass

if __name__ == '__main__':
    unittest.main()