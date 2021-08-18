# encoding=utf-8

from ddl.json import parse_json_keys

def test_parse_json_keys():

    d={
        "a":3,
        "c":{
           "d":5
        }
    }

    result = parse_json_keys(d)
    assert len(result)==2
    print('============================')
    print(',\n'.join(result))
