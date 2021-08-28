import { timeStamp } from 'console';
import React, { useState } from 'react';
import './index';

type JsonComment={
    data:string,
    hiveddl?:string,
    code?:number,
    error:string
}

export default class ParserJsonComment extends React.Component<{},JsonComment> {

  constructor(props: any) {
    super(props);
    this.state = {
        data:'',
        hiveddl:"",
        code:200,
        error:''
    };
    this.handleSubmit = this.handleSubmit.bind(this);
    this.data_change = this.data_change.bind(this);
    }

    handleSubmit(event:any) {
      // 请求后端处理
      let out = JSON.stringify({
        'data': this.state.data,
     })

      console.log(out)
      var xhr = new XMLHttpRequest();
      xhr.timeout = 3000;
      xhr.ontimeout = function (event) {
          alert("请求超时！");
      }

      xhr.onreadystatechange =
          () => {
              if (xhr.readyState == 4 && xhr.status == 200) {
                  var data: JsonComment = JSON.parse(xhr.responseText) as JsonComment
                  if (data.code != 200){
                    window.alert(data.error)
                  }
                  this.setState(data)
              }
          }

      xhr.open('POST', 'http://localhost:8085/jsoncommnet2ddl');
      xhr.send(out);
      event.preventDefault();

  }

data_change(event:any){
  this.setState(this.state && {'data':event.target.value})
} 

  render() {
    return (
      <div>
          <form onSubmit={this.handleSubmit}>
          <h3>json</h3>
          <textarea className='code_form'  value={this.state.data} onChange={this.data_change}>
          </textarea>
          <br/>
          <div>
              <input type="submit" value="提交" />
          </div>
        </form>
        <h2>hive_ddl</h2>
        <textarea className='code_form' value={this.state.hiveddl} >
        </textarea>
      </div>
    );
  }
};
