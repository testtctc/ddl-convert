# encoding=utf-8

#coding=utf-8
import json
from flask import render_template, Flask,request
from flask_cors import cross_origin
from ddl.parse import ColumnsExtract
from ddl.utils import generate_date_range

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


if __name__ == '__main__':
    app.run("0.0.0.0",8085,debug=True)