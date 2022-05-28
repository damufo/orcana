# -*- coding: utf-8 -*- 


import os
import csv
import gzip
from . import utils


def normalize_file_name(file_name):
    return utils.normalize_file_name(file_name)

def get_file_content(file_path, mode="all", compressed=True,
                     encoding=None, delimiter=","):
    '''
    open and read file
    mode = [all:read|lines:readlines]
    '''
    content = ""
    if os.path.isfile(file_path):
        if compressed:
            fil = gzip.open(file_path, 'rb')  # , encoding=encoding
            if mode == "all":
                if encoding:
                    content = fil.read().decode(encoding)
                else:
                    content = fil.read().decode()
            elif mode == "csv":
                input_file = csv.reader(fil, delimiter=delimiter)
                content = [line for line in input_file]
            else:
                if encoding:
                    content = [i.decode(encoding) for i in fil.readlines()]
                else:
                    content = [i.decode() for i in fil.readlines()]
        else:
            fil = open(file_path, 'r', encoding=encoding)
            if mode == "all":
                content = fil.read()
            elif mode == "csv":
                input_file = csv.reader(fil, delimiter=delimiter)
                content = [line for line in input_file]
            else:
                content = fil.readlines()
        fil.close()
        content = content  # .decode('utf-8')
    return content


def set_file_content(content, file_path, compress=True, binary=False,
                     encoding=None, end_line="\n"):
    '''
    write content to file. Content can be string or list/tuple strings
    binary (only for no compress), when true 'wb' when false 'w'
    compress: compress gzip
    encoding, example "ISO-8859-1"
    end_line: [\n | \r\n]
    '''

    if compress or binary:
        if compress:
            fil = gzip.open('{}.gz'.format(file_path), 'wb', encoding=encoding)
        else:
            fil = open(file_path, 'wb', encoding=encoding)

        if isinstance(content, (list, tuple)):
            for i in content:
                fil.write("{}{}".format(i, end_line).encode())
        elif isinstance(content, str):
            fil.write(content.encode())

    else:
        fil = open(file_path, 'w', encoding=encoding)

        if isinstance(content, (list, tuple)):
            for i in content:
                fil.write("{}{}".format(i, end_line))
        elif isinstance(content, str):
            fil.write(content)
    fil.close()


def parse_line(line, separator='#'):
    '''
    line: unicode string
    return unicode fields
    '''
    value = line.strip()
    value = value.replace('[/n]', "\n")
#     value = str(value, 'utf-8').split(separator) python2
    value = value.split(separator)

    return value


def parse_lines(lines, separator='#'):
    '''
    line: unicode string
    return unicode list of fields
    '''
    lines_parsed = []
    for i in lines:
        lines_parsed.append(parse_line(line=i, separator=separator))
    return lines_parsed


def export_table_to_file(dbs, tables, file_path, where_sql='', where_values=()):
    '''
    export to file to share
    tables is a tuple of tables
    '''

    content = ""
    for table_name in tables:
        sql = "select * from {} {}"
        sql = sql.format(table_name, where_sql)
        res = dbs.exec_sql(sql=sql, values=(where_values,))
        if res:
            content += "#**#%s\n" % (table_name)
            for i in res:
                line = ''
                for n in i:
                    campo = str(n)
                    campo = campo.replace("#", "-")
                    line = "%s%s#" % (line, campo)
                line = "%s" % (line[:(len(line)-1)],)
                line = line.replace('\n', "[/n]")  # Engadido para evitar
                # retornos de carro nos ficheiros intermedios
                line = line.replace('\u2018', ",")
                line = line.replace('\u2019', ",")
                line = line.replace('\u201c', '"')
                line = line.replace('\u201d', '"')
                line = line.replace("False", "0")
                line = line.replace("True",  "1")
                line = line.replace("None", "")
                content += "%s\n" % line
            print("Feito %s" % table_name)
    content = content

    set_file_content(content=content, file_path=file_path, compress=True)
