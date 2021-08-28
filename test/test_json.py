# encoding=utf-8

from ddl.json import parse_json_keys,parse_json_tuple,_parse_json
def test_parse_json_keys():
    d={
        "a":3,
        "c":{
           "e":5,
            "k":[3]
        },
        "d":"hello"
    }

    result = parse_json_keys(d)
    print('============================')
    print(',\n'.join(result))

    result2= parse_json_tuple(d)
    print('\n'.join(result2))

    out = _parse_json(d)
    print(out)



