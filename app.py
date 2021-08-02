# encoding=utf-8

#coding=utf-8
import json
from flask import render_template, Flask, Response,request
from flask_cors import cross_origin
import base64
from ddl.parse import ColumnsExtract

app = Flask(__name__,template_folder='webddl/build',static_folder='webddl/build/static')
app.config["COMPRESS_MIMETYPES"] =['application/json','application/javascript','text/css']

from flask_compress import Compress

compress = Compress()

compress.init_app(app)


@app.route("/data")
def provide_data():
    return json.dumps({"url":"www.baidu.com","name":"tc","email":"tangcheng2014@163.com"})

@app.route("/health")
def health():
    return "ok"

@app.route("/index")
def index():
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
    return json.dumps(out)


if __name__ == '__main__':
    app.run("0.0.0.0",8085,debug=True)