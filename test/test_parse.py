# encoding=utf-8
import re
from ddl.parse import ColumnsExtract

COLDEF= re.compile("""(`?\w+`?)\s+(\w+).*?(comment\s+(?P<quote>['"])(.*?)(?P=quote))?\s*,?$""",re.IGNORECASE)
def test_re():
    statement='id integer primary key comment "主键" ,'
    res= COLDEF.match(statement)
    print(res.group(5))
    assert  1==1

def test_parse():
    SQL = """
    CREATE TABLE foo (
             id integer primary key comment '主键',
             title varchar(200) not null,
             `description` text,
             `salary` FLOAT,
             key(title,description)
             );
    """

    parser = ColumnsExtract(SQL)
    parser.parse()
    print(parser.table_name)
    print(parser.comments)
    print(parser.coltypes)
    print(parser.formatted_columns())
    print(parser.formatted_columns('"',',\n'))
    ddl1 = parser.to_hive_ddl()
    ddl2=parser.to_doris_ddl()
    print(ddl2)