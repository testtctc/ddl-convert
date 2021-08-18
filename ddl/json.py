# encoding=utf-8

ROOT='$.'
FUNCTION='get_json_object'
VARIABLE='log'

def parse_json_keys(data:dict,start=ROOT,function=FUNCTION,variable = VARIABLE):
    result=[]
    for key  in data:
        if not isinstance(data[key],dict):
            result.append("{}({},'{}') as {}".format(function,variable,start+key,key))
        else:
            result.extend(parse_json_keys(data[key],start=start+key+'.'))
    return result



