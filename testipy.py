#!/usr/bin/env python3.4

import datetime
import os
import pickle
import pprint
import re
import sqlite3 as sql
import sys
import time
import tkinter
import traceback

## UTILS
import yaml
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

def read_yaml(filename_yaml):
    stream = open(filename_yaml, 'r')
    data = yaml.load(stream, Loader=Loader)
    return data


## GUI
class Window(object):
    def __init__(self):
        self.WIN = tkinter.Tk()
        self.prtcl_name = ''
        self.func = ''
        self.title = '' 
        self.xy = [0,0]
        self.config_file = 'testipy.yaml'

    def window_closed(self):
        self.WIN.destroy()

    def window_show(self):
        self.WIN.deiconify()

    # this is to control conf options
    # DEFAULTS:
    # prtcl_name 'WM_DELETE_WINDOW'
    # func window_closed
    # title "Someone's titley string"
    # x 500
    # y 200
    def configure(self, prtcl_name, resize, func, title, x, y):
        self.WIN.protocol(prtcl_name, func)
        self.WIN.wm_title(title)
        self.WIN.resizable(x,y)

    def auto_configure(self):
        self.yaml_dump = read_yaml(self.config_file)
        cfg_data = self.yaml_dump
        prtcl_name = cfg_data["protocol"]
        resize = cfg_data["resizeable"]
        func = self.window_closed
        title = cfg_data["title"]
        x = cfg_data["width"]
        y = cfg_data["height"]
        self.configure(
            prtcl_name,
            resize,
            func,
            title,
            x,y
            )

class Dialog(object):

    def __init__(self, main, info, title):

        top = self.top = tkinter.Toplevel(main)
        top.wm_title(title)
        tkinter.Label(top, text=info).pack()

        button = tkinter.Button(top,text="OK",command=self.ok)
        button.pack(pady=5)

    def ok(self):
        main.WIN.deiconify()
        self.top.destroy()


## MAIN 

class AppGUI(object):

    def __init__(self, main):
        self.label_dir_path = tkinter.Label(main.WIN,text="Path to directory:")
        self.label_dir_path.grid(row=0,column=0)

        self.dir_path_input = tkinter.StringVar()
        self.dir_path_entry = tkinter.Entry(main.WIN,textvariable=self.dir_path_input)
        self.dir_path_entry.grid(row=0,column=1)

        self.label_log_path = tkinter.Label(main.WIN,text="Path to logfile:")
        self.label_log_path.grid(row=1,column=0)

        self.log_path_input = tkinter.StringVar()
        self.log_path_entry = tkinter.Entry(main.WIN,textvariable=self.log_path_input)
        self.log_path_entry.grid(row=1,column=1)

        self.label_check = tkinter.Label(main.WIN,text="Yes. Have some.:")
        self.label_check.grid(row=2,column=0)

        self.check_var = tkinter.IntVar()

        self.checkbutton_get_ref_list = tkinter.Checkbutton(main.WIN,variable=self.check_var)
        self.checkbutton_get_ref_list.grid(row=2,column=1)

        self.go_button = tkinter.Button(main.WIN,text="GO!",command=self.go_callback,width=15)
        self.go_button.grid(row=3,column=0)

        self.chk_input_button = tkinter.Button(main.WIN,text="Check input",command=self.check_input,width=15)
        self.chk_input_button.grid(row=3,column=1)

        self.main = main

        self.main.WIN.mainloop()

    def go_callback(self):
        dialog = self.spawn_dialog("<default go callback msg>", "DEFAULT TITLE!!1")
        self.main.WIN.wait_window(dialog.top)

    def spawn_dialog(self, msg, title):
        dialog = Dialog(self.main.WIN, msg, title)
        return dialog

    def convert_check_to_bool(self, check_val):
        if check_val == 1:
            return True
        elif check_val == 0:
            return False
        else:
            print(traceback.format_exc())
            raise Exception(
                "convert_check_to_bool failed, " +
                "check_input param != 1 or 0. Instead got " + 
                repr(check_val)
                )

    def check_input(self):
        check_val = self.convert_check_to_bool(self.check_var.get())
        input_string = (
        "Directory path: " +
        self.dir_path_input.get() +
        "\n" +
        "Log path: " +
        self.log_path_input.get() +
        "\n" +
        "Checked?: " +
        str(check_val)
        )
        dialog = self.spawn_dialog(input_string, "Check input??/")
        self.main.WIN.wait_window(dialog.top)

## DB FUNCS
# ".+\.db" db filename regex
class DBHelper(object):
    def __init__(self, db_filename):
        self.db = db_filename
        self.con = False

    def open_con(self):
        if not self.con:
            try:
                self.con = sql.connect(self.db)
                return self.con 
            except sql.Error as e:
                print("Error: %s" % e.args[0])
        else:
            print("Connection already opened.")

    def close_con(self):
        if self.con:
            try:
                self.con.close()
            except sql.Error as e:
                print("Error: %s" % e.args[0])
        else:
            print("No open connection to close.")

    def cursor(self):
        if self.con:
            self.c = False
            try:
                self.c = self.con.cursor()
            except sql.Error as e:
                print("Error: %s" % e.args[0])
            return self.c
        else:
            print("No open connection for cursor.")

    def db_version(self):
        sqlite_vtext = "\nSQLite Version: "
        version = sqlite_vtext + "Unknown"
        try:
            self.open_con()
            self.cursor()
            self.c.execute('SELECT SQLITE_VERSION()')
            version = self.c.fetchone()[0]
        except sql.Error as e:
            print("Error: %s" % e.args[0])
        finally:
            self.close_con()
        return sqlite_vtext + version


# def create_creature_table(db):
#     commands = [
#         'DROP TABLE IF EXISTS creatures;',
#         '''CREATE TABLE IF NOT EXISTS creatures (
#             ID INTEGER PRIMARY KEY AUTOINCREMENT,
#             date text,
#             name text,
#             description text,
#             stats text,
#             type text,
#             pickled_obj text
#             );'''
#     ]
#     return db_commit(db, commands)

# def create_area_table(db):
#     commands = [
#         'DROP TABLE IF EXISTS areas;',
#         '''CREATE TABLE IF NOT EXISTS areas (
#             ID INTEGER PRIMARY KEY AUTOINCREMENT,
#             date text,
#             name text,
#             description text,
#             stats text,
#             type text,
#             pickled_obj text
#             );'''
#     ]
#     return db_commit(db, commands)

# def db_call(db, commands, method):
#     result = []
#     try:
#         con = sql.connect(db)
#         c = con.cursor()
#         import pdb; pdb.set_trace()
#         try:
#             for command in commands:
#                 c.execute(command)
#             if method == 'commit':
#                 result = con.commit()
#             elif method == 'fetch':
#                 result = c.fetchall()
#         except:
#             print traceback.format_exc()
#     except:
#         print traceback.format_exc()
#     finally:
#         if con:
#             con.close()
#         return result

# def db_commit(db, commands):
#     return db_call(db, commands, 'commit')

# def db_query(db, queries):
#     return db_call(db, queries, 'fetch')

# def get_tables(db):
#     queries = ["SELECT * FROM sqlite_master WHERE type='table';"]
#     return db_query(db, queries)

# def save_creature(db, creature):
#     pickled_creature = pickle.dumps(creature)
#     insert_statement = (
#         ('INSERT INTO creatures VALUES (' +
#         '{0}, {1}, {2}, {3}, {4}, {5}' +
#         ');').format(
#         creature.creation_date.strftime('%-m/%-d/%Y'),
#         creature.name,
#         creature.description,
#         repr(creature.stats),
#         creature.type,
#         pickled_creature
#         )
#     print 'arrived here...'
#     import pdb; pdb.set_trace()
#     db_commit(db, [insert_statement])

# def db_load(db, creature):
#     import pdb; pdb.set_trace()


    # #TODO
    # #implement more buttons

if __name__ == '__main__':
    main = Window()
    main.auto_configure()
    gui = AppGUI(main)