#!/usr/bin/env python3.4


import sys
import re
import sqlite3 as sql
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

    def test_open_con(self):
        self.dbh.open_con()
        if not self.dbh.con:
            raise Exception("Test failed, no open connection.")

    def test_close_con(self):
        self.dbh.open_con()
        self.dbh.close_con()
        try:
            self.dbh.con.cursor()
            self.dbh.c.execute('SELECT SQLITE_VERSION()')
            raise Exception('Connection open when expected to be closed.')
        except sql.Error as e:
            if e.__str__() == 'Cannot operate on a closed database.':
                pass
            else:
                print("Error: %s" % e.args[0])
                raise Exception('Unexpected error.')

    def test_cursor(self):
        self.dbh.open_con()
        try:
            self.dbh.cursor()
            self.dbh.c.execute('SELECT SQLITE_VERSION()')
            if '<sqlite3.Cursor object at' in self.dbh.c.__str__():
                pass
            else:
                raise Exception("'<sqlite3.Cursor object at' not found in " + self.dbh.c.__str__())
        except sql.Error as e:
            print("Error: %s" % e.args[0])
            raise Exception('Unexpected error.')

    def test_db_version(self):
        version = self.dbh.db_version()
        match = re.search('SQLite Version: \d.\d.\d.\d', version)
        if match:
            print(version)
        else:
            print(traceback.format_exc())
            raise Exception('No sqlite3 version regex match.')

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestipyDBTests)
    unittest.TextTestRunner(verbosity=2).run(suite)