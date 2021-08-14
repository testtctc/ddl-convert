import React from "react";
import './index'


// 状态
type NameFormState = {
    mysql_dll: string,
    cols_list: string,
    cols_str: string
    hive_ddl: string,
    flink_ddl:string,
    doris_ddl:string
}


export default class MysqlForm extends React.Component<{}, NameFormState> {
    constructor(props: any) {
        super(props);
        this.state = {
            mysql_dll: '',
            cols_list: '',
            cols_str: '',
            hive_ddl: '',
            flink_ddl:'',
            doris_ddl:''
        };


        this.handle_mysql_Change = this.handle_mysql_Change.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    handle_mysql_Change(event: any) {
        this.setState({ mysql_dll: event.target.value });
    }

    handleSubmit(event: any) {
        // 请求后端处理

        var out = JSON.stringify({ 'mysql_ddl': this.state.mysql_dll })
        console.log(out)
        var xhr = new XMLHttpRequest();
        xhr.timeout = 3000;
        xhr.ontimeout = function (event) {
            alert("请求超时！");
        }
        xhr.onreadystatechange =
            () => {
                if (xhr.readyState == 4 && xhr.status == 200) {
                    var data: NameFormState = JSON.parse(xhr.responseText) as NameFormState
                    this.setState(data)
                    console.log(this.state)
                }
            }

        xhr.open('POST', 'http://localhost:8085/hive_ddl');
        xhr.send(out);
        event.preventDefault();

    }

    render() {
        return (
            <form onSubmit={this.handleSubmit}>
                <label>
                    <div>
                        <input type="submit" value="转换 dll" />
                    </div>
                    <br/>
                    <label className='col_label' >mysql ddl</label>
                    <label>
                        <textarea className='code_form' value={this.state.mysql_dll} onChange={this.handle_mysql_Change} />
                    </label>
                    <label className='col_label'>columns list</label>
                    <label>
                        <textarea className='columns' value={this.state.cols_list} />
                    </label>
                    <br />
                    <label className='col_label' >hive ddl</label>
                    <label>
                        <textarea className='code_form' value={this.state.hive_ddl} />
                    </label>
                    <label className='col_label'>columns string</label>
                    <label>
                        <textarea className='columns' value={this.state.cols_str} />
                    </label>
                    <br/>
                    <br/>
                    <label className='col_label' >flink ddl</label>
                    <label>
                        <textarea className='code_form' value={this.state.flink_ddl} />
                    </label>
                    <br/>
                    <br/>
                    <label className='col_label' >doris ddl</label>
                    <label>
                        <textarea className='code_form' value={this.state.doris_ddl} />
                    </label>
                </label>
            </form>
        );
    }
}