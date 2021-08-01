# encoding=utf-8
# !/usr/bin/env python
#
# Copyright (C) 2009-2020 the sqlparse authors and contributors
# <see AUTHORS file>
#
# This example is part of python-sqlparse and is released under
# the BSD License: https://opensource.org/licenses/BSD-3-Clause
#
# Example for retrieving column definitions from a CREATE statement
# using low-level functions.

# !/usr/bin/env python
#
# Copyright (C) 2009-2020 the sqlparse authors and contributors
# <see AUTHORS file>
#
# This example is part of python-sqlparse and is released under
# the BSD License: https://opensource.org/licenses/BSD-3-Clause
#
# Example for retrieving column definitions from a CREATE statement
# using low-level functions.


import sqlparse
import re
import logging

from sqlparse.sql import TokenList
from sqlparse.tokens import Punctuation

HIVE_TYPE_MAPS = {
    'DECIMAL': 'DECIMAL',
    'FLOAT': 'FLOAT',
    'TINYINT': 'TINYINT',
    'INT': 'INT',
    'INTEGER': 'INT',
    'SMALLINT': 'SMALLINT',
    'DOUBLE': 'DOUBLE',
    'TIMESTAMP': 'BIGINT',
    'DATE': 'DATE',
    'YEAR': 'INT',
    'DATETIME': 'STRING',
    'TIME': 'STRING',
    'CHAR': 'STRING',
    'VARCHAR': 'STRING',
    'TEXT': 'STRING',
    'TINYTEXT': 'STRING',
    'MEDIUMTEXT': 'STRING',
    'LONGTEXT': 'STRING',
    'BLOB': 'STRING',
    'TINYBLOB': 'STRING',
    'MEDIUMBLOB': 'STRING',
    'LONGBLOB': 'STRING',
    'JSON': 'STRING'
}

COLDEF= re.compile("""`?(\w+)`?\s+(\w+).*?(comment\s+(?P<quote>['"])(.*?)(?P=quote))?\s*,?$""",re.IGNORECASE)
CREATE_TABLE=re.compile(r"create\s+table\s+(\w+\.)?(\w+)",re.IGNORECASE)


class ColumnsExtract():

    def __init__(self, sql: str):
        """
        sql:建表语句
        """
        assert re.match('create\s+table', sql.strip(), flags=re.IGNORECASE)

        self.table_name=None

        self.sql = sql.strip()
        # 列
        self.columnames = []
        self.coltypes={}
        self.comments={}
        # 定义
        self.definitions = {}
        #是否完成解析
        self.parsed=False

    def parse(self):
        parsed = sqlparse.parse(self.sql)[0]

        # extract the parenthesis which holds column definitions
        self.table_name=CREATE_TABLE.match(self.sql).group(2)
        pos, par = parsed.token_next_by(i=sqlparse.sql.Parenthesis)

        self.extract_definitions(par)
        print(self.definitions)
        self.parsed=True

    def extract_definitions(self, token_list: TokenList):
        # assumes that token_list is a parenthesis
        definitions = []
        tmp = []
        ##解析深度
        par_level = 0
        start = 1
        flatened = [t for t in token_list.flatten()]
        new_token_list=TokenList(flatened)
        end = len(flatened)
        while True:
            pos, _ = new_token_list.token_next_by(m=(Punctuation, ','), idx=start)

            #控制位移

            if pos:
                statement = flatened[start:pos]
                start = pos+1
            else:
                statement = flatened[pos:end]

            statement=''.join(str(i) for i in statement).strip()
            #print(statement)
            res=COLDEF.match(statement)
            if res:
                colname=res.group(1)
                coltype=res.group(2).upper()
                colcomment=res.group(5)  if res.group(5) else ''

                self.columnames.append(colname)
                self.definitions[colname]=statement
                self.coltypes[colname]=coltype
                self.comments[colname]=colcomment

            else:
                #无法匹配时，则直接放弃
                break

    def formatted_columns(self, quoted_by='`', seperated_by=','):
        cols = ['{}{}{}'.format(quoted_by,c,quoted_by) for c in self.columnames]
        return seperated_by.join(cols)


    def to_hive_ddl(self):
        if not self.parsed:
            raise ValueError('please parse the ddl')

        template = "create table {table}(\n{columns}\n);"
        columns=[  "{} {} comment  '{}' ".format(c,HIVE_TYPE_MAPS[self.coltypes[c]],self.comments[c]) for c in self.columnames]
        columns= ',\n'.join(columns)
        res = template.format(table=self.table_name,columns=columns)
        return res
9