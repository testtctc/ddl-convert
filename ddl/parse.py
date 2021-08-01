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

TYPES = {
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

COLDEF= re.compile("""(`?\w+`?)\s+(\w+).*?(comment\s+(?P<quote>['"])(.*?)(?P=quote))?\s*,?$""",re.IGNORECASE)

class ColumnsExtract():

    def __init__(self, sql: str):
        """
        sql:建表语句
        """
        assert re.match('create\s+table', sql.strip(), flags=re.IGNORECASE)
        self.sql = sql
        # 列
        self.columnames = []
        # 定义
        self.definitions = {}

    def parse(self):
        parsed = sqlparse.parse(self.sql)[0]

        # extract the parenthesis which holds column definitions
        pos, par = parsed.token_next_by(i=sqlparse.sql.Parenthesis)
        self.extract_definitions(par)
        print(self.definitions)

    def extract_definitions(self, token_list: TokenList):
        # assumes that token_list is a parenthesis
        definitions = []
        tmp = []
        ##解析深度
        par_level = 0
        start = 1
        flatened = [t for t in token_list.flatten()]
        end = len(flatened)
        while True:
            pos, _ = token_list.token_next_by(m=(Punctuation, ','), idx=start)
            if pos:
                statement = flatened[start:pos]
                start = pos
            else:
                statement = flatened[pos:end]
            statement=''.join(str(i) for i in statement).strip()
            print(statement)
            res=COLDEF.match(statement)
            if res:
                colname=res.group(1)
                coltype=res.group(2).upper()
                colcomment=res.group(5)  if res.group(5) else ''

                self.columnames.append(colname)
                self.definitions[colname]=statement
            else:
                #无法匹配时，则直接放弃
                break

        # for token in token_list.flatten():
        #     if token.is_whitespace:
        #         continue
        #     elif token.match(sqlparse.tokens.Punctuation, '('):
        #         par_level += 1
        #         continue
        #     if token.match(sqlparse.tokens.Punctuation, ')'):
        #         if par_level == 0:
        #             break
        #         else:
        #             par_level -= 1
        #     elif token.match(sqlparse.tokens.Punctuation, ','):
        #         if tmp:
        #             definitions.append(tmp)
        #         tmp = []
        #     else:
        #         tmp.append(token)
        # if tmp:
        #     definitions.append(tmp)
        # return definitions

    @property
    def formatted_columns(self, quoted_by='`', seperated_by=','):
        cols = ['`{}`'.format(c) for c in self.columnames]
        return seperated_by.join(cols)


if __name__ == '__main__':
    SQL = """CREATE TABLE foo (
             id integer primary key comment '主键',
             title varchar(200) not null,
             description text,
             `salary` FLOAT,
             key(title,description)
             );"""

    parser = ColumnsExtract(SQL)
    parser.parse()
    print(parser.formatted_columns)
