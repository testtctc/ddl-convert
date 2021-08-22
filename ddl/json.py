# encoding=utf-8

ROOT='$.'
FUNCTION='get_json_object'
VARIABLE='log'
LEVEL=0

def parse_json_keys(data:dict,start=ROOT,function=FUNCTION,variable = VARIABLE):
    result=[]
    for key  in data:
        if not isinstance(data[key],dict):
            result.append("{}({},'{}') as {}".format(function,variable,start+key,key))
        else:
            result.extend(parse_json_keys(data[key],start=start+key+'.'))
    return result

def parse_json_tuple(data:dict,start=ROOT,function=FUNCTION,variable = VARIABLE):
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