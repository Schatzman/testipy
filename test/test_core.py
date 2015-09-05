#!/usr/bin/env python3.4
import re
import sqlite3 as sql
import sys
import traceback
import unittest

# append ../ to path based on os to import from testipy folder
if sys.platform == 'win32':
    sys.path.append('..\\')
elif sys.platform == 'darwin':
    sys.path.append('../')
else:
    print("Hmmm.... unknown platform. What is %s?" % sys.platform)
from DB import DBHelper
from util.db import *

def callback():
    return True

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
            pass # test passes
        else:
            print(traceback.format_exc())
            raise Exception('No sqlite3 version regex match.')

    def test_db_call_commit(self): # this is silly.
        commands = [
            "ATTACH 'test.db' as test",
            'DROP TABLE IF EXISTS test.test_table',
            '''CREATE TABLE IF NOT EXISTS test.test_table (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date text NULL,
                name text NULL,
                description text NULL,
                pickled_obj text NULL
                );'''
        ]
        try:
            self.dbh.open_con()
            self.dbh.cursor()
            for command in commands:
                self.dbh.c.execute(command)
            self.dbh.con.commit()
        except sql.Error as e:
            print("Error: %s" % e.args[0])
            print(traceback.format_exc())
            raise Exception("SQL ERROR. TEST FAILED.")
        finally:
            self.dbh.close_con()

# recall the ../ appended to path during initial imports...

from GUI import AppGUI
from GUI import Window
from pprint import pprint

class TestipyGUITests(unittest.TestCase):
    """
    Tests relating to graphical user interface functionality.
    """

    def setUp(self):
        self.main = Window()
        # self.main.auto_configure()
        self.gui = AppGUI(self.main, True)

    def tearDown(self):
        try:
            self.main.WIN.destroy()
        except:
            pass # sometimes it has already been destroyed.

    def test_WIN(self):
        item_on_test = self.main.WIN
        if '<tkinter.Tk object at' in repr(item_on_test):
            pass
        else:
            raise Exception(
                'Something went wrong, is this a tkinter.Tk object?: ' +
                repr(item_on_test)
                )

    def test_window_closed(self):
        self.main.window_closed()
        err = ''
        try:
            self.main.WIN.winfo_exists()
        except Exception as e:
            err = e.__str__()
            expected = (
                'application has been destroyed'
                )
            err_lst = []
            self.assertTrue(expected in err)

    def test_window_show(self):
        self.main.WIN.withdraw()
        self.assertEqual(self.main.WIN.state(), 'withdrawn')
        self.main.window_show()
        self.assertEqual(self.main.WIN.state(), 'normal')

    def test_configure(self):
        print("PRE CONFIGURE")
        print(self.main.WIN.winfo_width())
        print(self.main.WIN.winfo_height())
        print(self.main.WIN.title())
        print(self.main.WIN.wm_protocol()) # 'WM_DELETE_WINDOW'
        print(self.main.WIN.wm_resizable()) # (1,1) = resize x True, resize y True

        import time
        time.sleep(1)
        prtcl_name = "WM_DELETE_WINDOW"
        resize = True
        func = callback
        title = "TESTY McTesterWindow"
        x = 1000
        y = 1000
        self.main.configure(
            prtcl_name,
            resize,
            func,
            title,
            x, y
            )
        time.sleep(1)
        print("POST CONFIGURE")
        print(self.main.WIN.winfo_width())
        print(self.main.WIN.winfo_height())
        print(self.main.WIN.title())
        print(self.main.WIN.wm_protocol()) # 'WM_DELETE_WINDOW'
        print(self.main.WIN.wm_resizable())
        # check resizable
        # check protocol
        # check wm_title
        # configure
        # check that new values are set.
        # fixme
        import pdb; pdb.set_trace()

    def test_autoconfigure(self):
        # test pulling conf values from yaml.
        # fixme
        pass

    def test_GUI(self):
        item_on_test = self.gui
        if '<GUI.AppGUI object at' in repr(item_on_test):
            pass
        else:
            raise Exception(
                'Something went wrong, is this a GUI.AppGUI object?: ' +
                repr(item_on_test)
                )

    def test_main(self):
        item_on_test = self.main
        if '<GUI.Window object at' in repr(item_on_test):
            pass
        else:
            raise Exception(
                'Something went wrong, is this a GUI.Window object?: ' +
                repr(item_on_test)
                )


if __name__ == '__main__':
    testsuites = [TestipyDBTests, TestipyGUITests]
    for testcases in testsuites:
        suite = unittest.TestLoader().loadTestsFromTestCase(testcases)
        unittest.TextTestRunner(verbosity=2).run(suite)
