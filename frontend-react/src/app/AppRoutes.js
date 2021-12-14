import React from "react";
import { Route, Switch, Redirect } from 'react-router-dom';
import Home from "../components/Home";
import Forecast from "../components/Forecast";
import Agent from "../components/Agent";
import Error404 from '../components/Error/404';

const AppRouter = (props) => {

  console.log("================================== AppRouter ======================================");

  return (
    <React.Fragment>
      <Switch>
        <Route path="/" exact component={Home} />
        <Route path="/forecast" exact component={Forecast} />
        <Route path="/agent" exact component={Agent} />
        <Route component={Error404} />
      </Switch>
    </React.Fragment>
  );
}

export default AppRouter;