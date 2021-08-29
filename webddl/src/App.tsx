import React from 'react';
import logo from './logo.svg';
import './App.css';
import MysqlForm from './form'
import DorisDates from './dorisdates'
import ExtractJsonKeys from './jsonkeys'

import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link
} from "react-router-dom";
import ParserJsonComment from './json_comment_2_dll';
import ParserJson from './json_2_hiveddl';
import FormatJson from './format_json';
import { Showparamters } from './paramters';


function App() {
  return (
    <Router>
      <div>
        <nav>
          <ul>
            <li>
              <Link to="/">Home</Link>
            </li>
            <li>
              <Link to="/mysqlform">MysqlForm</Link>
            </li>
            <li>
              <Link to="/dorisdates">DorisDates</Link>
            </li>
            <li>
              <Link to="/jsonkeys">ExtractJsonKeys</Link>
            </li>
            <li>
              <Link to="/jsocommet">JsonCommet2HiveDdl</Link>
            </li>
            <li>
              <Link to="/json">Json2HiveDdl</Link>
            </li>
            <li>
              <Link to="/formatjson">FormatJson</Link>
            </li>
            <li>
              <Link to="/paramters">Showparamters</Link>
            </li>
          </ul>
        </nav>

        <Switch>
          <Route path="/jsonkeys">
            <ExtractJsonKeys />
          </Route>
          <Route path="/paramters">
            <Showparamters />
          </Route>
          <Route path="/formatjson">
            <FormatJson/>
          </Route>
          <Route path="/json">
            <ParserJson />
          </Route>
          <Route path="/jsocommet">
            <ParserJsonComment />
          </Route>
          <Route path="/mysqlform">
            <From />
          </Route>
          <Route path="/dorisdates">
            <DorisDates />
          </Route>
          <Route path="/">
            <Home />
          </Route>
        </Switch>
      </div>
    </Router>
  );

}

function Home() {
  return <h2>
    数仓常用工具
  </h2>;
}

function From() {
    return (
    <div className="App">
      <h1>
         mysql ddl 转化器
      </h1>
      <br/>
      <MysqlForm/>
    </div> );
}


export default App;
