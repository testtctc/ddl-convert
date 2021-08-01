# encoding=utf-8
import re

COLDEF= re.compile("""(`?\w+`?)\s+(\w+).*?(comment\s+(?P<quote>['"])(.*?)(?P=quote))?\s*,?$""",re.IGNORECASE)
def test_re():
    statement='id integer primary key comment "主键" ,'
    res= COLDEF.match(statement)
    print(res.group(5))
    assert  1==1