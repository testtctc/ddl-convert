import React from 'react';
import { getTextOfJSDocComment } from 'typescript';
import JsonEditor from './format_json2';

type JsonRaw={
    data:string,
    alldata:string
}

export default class FormatJson extends React.Component<{},JsonRaw> {
  constructor(props: any) {
    super(props);
    this.state = {
        data:`{ "bookname ":"VB BLACK BOOK", "price":500 }`,
        alldata:"{}"   
    };
    this.handleSubmit = this.handleSubmit.bind(this);
    this.data_change = this.data_change.bind(this);
    }

  handleSubmit(event:any) {
      // 请求后端处理
      this.setState(this.state && {"alldata":this.state.data} )
      event.preventDefault();
  }

  data_change(event:any){
   this.setState( this.state && {'data':event.target.value})
  } 

  render() {
    return (
      <div>
          <form onSubmit={this.handleSubmit}>
          <h3>json</h3>
          <textarea className='code_form' value={this.state.data} onChange={this.data_change}>
          </textarea>
          <br/>
          <div>
              <input type="submit" value="提交" />
          </div>
        </form>
        <JsonEditor text={this.state.alldata}/>
      </div>
    );
  }
};


