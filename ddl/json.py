# encoding=utf-8

ROOT='$.'
FUNCTION='get_json_object'
VARIABLE='log'
LEVEL=0

def parse_json_keys(data:dict,start=ROOT,function=FUNCTION,variable = VARIABLE):
    """a utility for hive function get_json_object """
    result=[]
    for key  in data:
        if not isinstance(data[key],dict):
            result.append("{}({},'{}') as {}".format(function,variable,start+key,key))
        else:
            result.extend(parse_json_keys(data[key],start=start+key+'.'))
    return result

def parse_json_tuple(data:dict,start=ROOT,function=FUNCTION,variable = VARIABLE):
    """ a utility for hive function lateral view  json_tuple """
    global LEVEL

    result=[]
    flat_keys=[]
    local_level=LEVEL
    for key in data:
        if not isinstance(data[key],dict):
            flat_keys.append(key)
        else:
            #新的解析对象
            v="{}({},'{}')".format(function,variable,start+key)
            LEVEL = LEVEL + 1
            result.extend(
                parse_json_tuple(
                    data=data[key],
                    start=start+key+'.',
                    variable=v
                )
            )

    statement='lateral view  json_tuple({var},{col_list}) t{level} as {col_list2}'.format(var=variable,
                                                                      col_list=','.join(["'"+k+"'" for k in flat_keys]),
                                                                      level=local_level,
                                                                      col_list2=','.join([k for k in flat_keys])
                                                                    )

    result.append(statement)
    return result


def parse_from_json(raw):
    """ a utility for spark function from_json"""

    assert (isinstance(raw,dict) or isinstance(raw,list))
    return _parse_json(raw)

def _parse_json(o):
    if isinstance(o, dict):
        l = []
        for k in o:
            if isinstance(o[k],dict):
                l.append( k +":" +  _parse_json(o[k])  )
            elif  isinstance(o[k],list):
                l.append(k + ':'+ _parse_json(o[k]))
            else:
                l.append( k +":"+ "string")
        return "strcut<"+ ",".join(l) +">"

    if isinstance(o,list):
        try:
            first = o[0]
            return  "array<" + _parse_json(_parse_json(first)) + ">"
        except IndexError:
            return "array<string>"
    else:
        return "string"