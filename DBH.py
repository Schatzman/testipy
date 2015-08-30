import pickle
import sqlite3 as sql

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