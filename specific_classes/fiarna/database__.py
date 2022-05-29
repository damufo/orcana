# -*- coding: utf-8 -*-

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

# Copyright (C) 2017 Federacion Galega de Natación (FEGAN) http://www.fegan.org
# Author: Daniel Muñiz Fontoira (2017) <dani@damufo.com>

import sys
import subprocess
# import win32com.client
# import adodbapi


class Database(object):

    def __init__(self, platform):
        """
        parm dict values
            type: access, sqlite, mysql
            path: only access and sqlite
            host: only mysql
            name: name database for mysql
            user: user mysql
            password: password mysql to connect
        """
        self.platform = platform
        self.conexion = None

    def connection(self, dbs_path):
        platform = self.platform
        if platform == "win":
            import adodbapi
            try:
                dsn = "Provider=Microsoft.Jet.OLEDB.4.0;Data Source={};User Id=admin;Password=;"
                dsn = dsn.format(dbs_path)
                conexion = adodbapi.connect(dsn)
            except:
                conexion = None
                print("Error no contemplado: ", sys.exc_info()[0])
        elif platform == "lin":
            conexion = dbs_path
        self.conexion = conexion

    def exec_sql(self, sql):
        rows = None
        if self.platform == "win":
            rows = self.exec_sql_win(sql=sql)
        elif self.platform == "lin":
            rows = self.exec_sql_lin(sql=sql)
        return rows

    def exec_sql_lin(self, sql):
        """
        sql: string sql
        """

        fields = []
        rows = []
        try:
            ps = subprocess.Popen(('echo', sql), stdout=subprocess.PIPE)
            output = subprocess.check_output(('mdb-sql', self.conexion),
                                             stdin=ps.stdout)

            lines = output.decode('utf8').split('\n')

            for i in lines:
                if len(i) and i[0] == "|":
                    if not fields:
                        fields = [j.strip() for j in i.split("|")[1:-1]]
                    else:
                        rows.append([j.strip() for j in i.split("|")[1:-1]])

        except:
            print("Error no contemplado: ", sys.exc_info()[0])
            print("Erro ao executar: ", sql)
            return "err"
        return rows

    def exec_sql_win(self, sql):
        """
        sql: string sql
        """
        try:
            cursor = self.conexion.cursor()
            cursor.execute(sql)
            rows = cursor.fetchall()
            cursor.close()
        except:
            print("Error no contemplado: ", sys.exc_info()[0])
            print("Erro ao executar: ", sql)
            return "err"
        return rows

    def close(self):
        """
        Close database.
        """
        self.conexion.close()
