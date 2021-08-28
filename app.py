# encoding=utf-8

#coding=utf-8
import json
from flask import render_template, Flask,request
from flask_cors import cross_origin

from ddl.json_to_ddl import JsonCommentToHiveDdl, JsonToHiveDdl
from ddl.parse import ColumnsExtract
from ddl.utils import generate_date_range
from ddl.json import parse_json_keys, parse_json_tuple, parse_from_json
import  traceback

app = Flask(__name__,template_folder='webddl/build',static_folder='webddl/build/static')
app.config["COMPRESS_MIMETYPES"] =['application/json','application/javascript','text/css']

from flask_compress import Compress

compress = Compress()

compress.init_app(app)

@app.route("/health")
def health():
    """检查健康"""
    return "ok"

@app.route("/index")
def index():
    """启动页面"""
    return render_template('index.html')


@app.route("/hive_ddl",methods=['POST'])
@cross_origin()
def hive_ddl():
    """mysql  dll  to hive ddl"""
    d = json.loads(request.data)
    print(d)
    sql = d['mysql_ddl']
    out={}
    parser = ColumnsExtract(sql)
    parser.parse()
    out['cols_list'] = parser.formatted_columns()
    out['cols_str']=parser.formatted_columns('"', ',\n')
    out['hive_ddl'] = parser.to_hive_ddl()
    out['mysql_ddl']=sql
    out['flink_ddl']=parser.to_flink_ddl()
    out['doris_ddl'] = parser.to_doris_ddl()
    return json.dumps(out)

@app.route("/dates",methods=['POST'])
@cross_origin()
def generate_dates():
    d = json.loads(request.data)
    print(d)
    start = d['start_date']
    end=d['end_date']
    dates = generate_date_range(start,end)
    out={
        "start_date":start,
        "end_date":end,
        "partitions":dates
    }
    return json.dumps(out)


@app.route("/parse_json_keys",methods=['POST'])
@cross_origin()
def generate_json_keys():
    d = json.loads(request.data)
    assert d is not None
    print(d)
    try:
        jsondata = json.loads(d['data'])
        get_json_object = ',\n'.join(parse_json_keys(jsondata))
        r= parse_json_tuple(jsondata)[::-1]
        json_tuple = '\n'.join(r)
        from_json = parse_from_json(jsondata)
        out = {
            "data": d['data'],
            "get_json_object": get_json_object,
            "json_tuple": json_tuple,
            "from_json":from_json,
            "error": "",
            "code": 200
        }
    except Exception as e:
        traceback.print_exc()
        out = {
            "data": d['data'],
            "get_json_object": '',
            "json_tuple": '',
            "from_json":'',
            "error":str(e),
            "code":300
        }
    return json.dumps(out)

@app.route("/jsoncommnet2ddl",methods=['POST'])
@cross_origin()
def jsoncommnet2ddl():
    d = json.loads(request.data)
    assert d is not None
    print(d)
    print('================test_json_comment_to_hive_ddl==========================')
    try:
        jsondata = json.loads(d['data'])
        parser = JsonCommentToHiveDdl(jsondata)
        hiveddl  = parser.to_hive_ddl()
        out = {
            "code": 200,
            "error": "",
             "hiveddl":hiveddl
        }
    except Exception as e:
        traceback.print_exc()
        out = {
            "hiveddl": "",
            "error":str(e),
            "code":300
        }
    print(out)
    return json.dumps(out)

@app.route("/json2ddl",methods=['POST'])
@cross_origin()
def json2ddl():
    d = json.loads(request.data)
    assert d is not None
    print(d)

    print('================test_json_comment_to_hive_ddl==========================')
    try:
        jsondata = json.loads(d['data'])
        parser = JsonToHiveDdl(jsondata)
        hiveddl = parser.to_hive_ddl()
        out = {
            "code": 200,
            "error": "",
            "hiveddl": hiveddl
        }
    except Exception as e:
        traceback.print_exc()
        out = {
            "hiveddl": "",
            "error": str(e),
            "code": 300
        }
    return json.dumps(out)


if __name__ == '__main__':
    app.run("0.0.0.0",8085,debug=True)