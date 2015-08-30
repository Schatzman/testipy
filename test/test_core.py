#!/usr/bin/env python3.4

import sys
import re
import sqlite3 as sql
import traceback
import unittest

# append ../ to path based on os to import from testipy folder
if sys.platform == 'win32':
    sys.path.append('..\\')
elif sys.platform == 'darwin':
    sys.path.append('../')
else:
    print("Hmmm.... unknown platform. What is %s?" % sys.platform)
from DBH import DBHelper
from util.db import *


class TestipyDBTests(unittest.TestCase):
    """
    Tests relating to database functionality.
    """

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

# recall the ../ appended to path during initial imports...
from GUI import AppGUI
from GUI import Window

class TestipyGUITests(unittest.TestCase):
    """
    Tests relating to graphical user interface functionality.
    """

    def setUp(self):
        self.main = Window()
        self.main.auto_configure()
        self.gui = AppGUI(self.main, True)

    def tearDown(self):
        try:
            self.main.WIN.destroy()
        except:
            print(traceback.format_exc())

    def test_WIN(self):
        if '<tkinter.Tk object at' in repr(self.main.WIN):
            pass
        else:
            raise Exception(
                'Something went wrong, is this a tkinter.Tk object?: ' +
                repr(self.main.WIN)
                )

    def test_GUI(self):
        if '<GUI.AppGUI object at' in repr(self.gui):
            pass
        else:
            raise Exception(
                'Something went wrong, is this a GUI.AppGUI object?: ' +
                repr(self.main.WIN)
                )

    def test_main(self):
        if '<GUI.Window object at' in repr(self.main):
            pass
        else:
            raise Exception(
                'Something went wrong, is this a GUI.Window object?: ' +
                repr(self.main.WIN)
                )


if __name__ == '__main__':
    testcases = [TestipyDBTests, TestipyGUITests]
    for testcase in testcases:
        suite = unittest.TestLoader().loadTestsFromTestCase(testcase)
        unittest.TextTestRunner(verbosity=2).run(suite)
