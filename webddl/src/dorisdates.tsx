import { timeStamp } from 'console';
import React, { useState } from 'react';
import Calendar from 'react-calendar';
import 'react-calendar/dist/Calendar.css';
import './index.css'

type DateRange={
    start_date:string,
    end_date:string,
    partitions:string
}

export default class DorisDates extends React.Component<{},DateRange> {

  constructor(props: any) {
    super(props);
    var now=this.DateToYYYYMMDD_HHMM(new Date());
    this.state = {
      start_date:now,
      end_date:now,
      partitions:''
    };
    this.handleSubmit = this.handleSubmit.bind(this);
    }

    handleSubmit(event: any) {
      // 请求后端处理
      let out = JSON.stringify({
        'start_date': this.state.start_date,
        'end_date':this.state.end_date
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
                  var data: DateRange = JSON.parse(xhr.responseText) as DateRange
                  console.log(data)
                  this.setState(data)
              }
          }

      xhr.open('POST', 'http://localhost:8085/dates');
      xhr.send(out);
      event.preventDefault();

  }

  DateToYYYYMMDD_HHMM(Date: Date): string {
    let DS: string = Date.getFullYear()
        + '-' + ('0' + (Date.getMonth() + 1)).slice(-2)
        + '-' + ('0' + Date.getDate()).slice(-2)
    return DS
}
  start_date_onChange=(value:Date)=>{
    this.setState( this.state && {'start_date':this.DateToYYYYMMDD_HHMM(value)}  )
  };
  end_date_onChange=(value:Date)=>{
    this.setState( this.state && {'end_date':this.DateToYYYYMMDD_HHMM(value)})
  }

  render() {
    return (
      <div>
        <p className='calendar'>
        <label>开始日期</label>
        <Calendar onChange={this.start_date_onChange} />
        <label>结束日期</label>
        <Calendar  onChange={this.end_date_onChange}/>
        </p>
        <label>
          <form onSubmit={this.handleSubmit}>
              <div>
                  <input type="submit" value="生成日期" />
              </div>
          </form>
          <pre>
            {this.state.partitions}
          </pre>
        </label>
      </div>
    );
  }

    
};
