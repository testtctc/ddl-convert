import { timeStamp } from 'console';
import React, { useState } from 'react';
import './index';

type JsonKeys={
    data:string,
    keys?:string,
}

export default class ExtractJsonKeys extends React.Component<{},JsonKeys> {

  constructor(props: any) {
    super(props);
    this.state = {
        data:'',
        keys:''
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
                  var data: JsonKeys = JSON.parse(xhr.responseText) as JsonKeys
                  console.log(data)
                  this.setState(data)
              }
          }

      xhr.open('POST', 'http://localhost:8085/parse_json_keys');
      xhr.send(out);
      event.preventDefault();

  }

data_change(event:any){
  this.setState(this.state && {'data':event.target.value})
} 

  render() {
    return (
      <div>
        <label>
            <form onSubmit={this.handleSubmit}>
            <h3>json</h3>
            <textarea className='code_form'  value={this.state.data} onChange={this.data_change}>
            </textarea>
            <br/>
            <div>
                <input type="submit" value="提交" />
            </div>
          </form>
          <pre>
            {this.state.keys}
          </pre>
        </label>
      </div>
    );
  }

    
};
