# -*- coding: utf-8 -*-


"""
SqlitePlus.
20200622. Version first.
"""
import sys
import sqlite3 as sqlite

# print(("pySQLite: ", sqlite.version))
# print(("SQLite: ", sqlite.sqlite_version))


class SqlitePlus(object):

    def __init__(self, dbs_path=None):
        if dbs_path:
            self.connect(dbs_path=dbs_path)
        else:
            self.dbs_path = None

    def connect(self, dbs_path):
        try:
            self.connection = sqlite.connect(dbs_path)
            cursor = self.connection.cursor()
            cursor.execute("PRAGMA cache_size=2000")
            cursor.execute('PRAGMA encoding="UTF-8";')
            self.connection.commit()
            cursor.close()
            self.dbs_path = dbs_path
        except BaseException:
            self.connection = None
            self.dbs_path = None

    def exec_sql(self, sql, values=None, n=0, thread=False):
        """
        sql: string sql
        values: tuple with values
        n: number items to get
        """
        if thread and dbs_path:
            connection = sqlite.connect(self.dbs_path)
        else:
            connection =  self.connection
        cursor = connection.cursor()

        tipo = sql.split()[0].lower()
        if tipo == "select":
            if values:
                if isinstance(values, (list, tuple)):
                    try:
                        cursor.execute(sql, values[0])
                    except BaseException:
                        print(("Error no contemplado:", sys.exc_info()[0]))
                        print(("Error no contemplado:", sys.exc_info()[1]))
                        print(("Erro ao executar: %s" % sql))
                        print(("Cos valores: ", values))
                        return "err"
                else:
                    try:
                        cursor.execute(sql, values)
                    except BaseException:
                        print(("Error no contemplado:", sys.exc_info()[0]))
                        print(("Error no contemplado:", sys.exc_info()[1]))
                        print(("Erro ao executar: %s" % sql))
                        print(("Cos valores: ", values))
                        return "err"
            else:
                try:
                    cursor.execute(sql)
                except BaseException:
                    print(("Error no contemplado:", sys.exc_info()[0]))
                    print(("Error no contemplado:", sys.exc_info()[1]))
                    print(("Erro ao executar: %s" % sql))
                    print("Sen valores")
                    return "err"
            if n == 0:
                return cursor.fetchall()
            else:
                return cursor.fetchmany(n)
        else:
            if values:
                for i in values:
                    try:
                        cursor.execute(sql, i)
                    except BaseException:
                        print(("Error no contemplado:", sys.exc_info()[0]))
                        print(("Error no contemplado:", sys.exc_info()[1]))
                        print(("Erro ao executar: %s" % sql))
                        print(("Cos valores: ", i))
                        return "err"
            else:
                try:
                    cursor.execute(sql)
                except BaseException:
                    print(("Error no contemplado:", sys.exc_info()[0]))
                    print(("Erro ao executar: %s" % sql))
                    return "err"
            connection.commit()
        cursor.close()

    def normalize(self, value):
        """
        for search
        """
        normalize = ("UPPER(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE("
                     "REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(%s,'Á',"
                     "'A'), 'É','E'),'Í','I'),'Ó','O'),'Ú','U'),'Ñ','N'),'á',"
                     "'a'), 'é','e'),'í','i'),'ó','o'),'ú','u'),'ñ','n'))")
        normalize = normalize % value
        return normalize

    def close(self):
        self.connection.close()

#    def compact(self):
#        self.cur.execute('VACUUM')
#        self.con.commit()
