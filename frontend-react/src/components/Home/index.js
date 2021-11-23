import InputLabel from '@material-ui/core/InputLabel';
import MenuItem from '@material-ui/core/MenuItem';
import FormHelperText from '@material-ui/core/FormHelperText';
import FormControl from '@material-ui/core/FormControl';
import Select from '@material-ui/core/Select';
import React, { useEffect, useRef, useState } from 'react';
import { withStyles } from '@material-ui/core';
import Container from '@material-ui/core/Container';
import Typography from '@material-ui/core/Typography';
import Grid from '@material-ui/core/Grid';
import Card from '@material-ui/core/Card';
import CardActions from '@material-ui/core/CardActions';
import CardContent from '@material-ui/core/CardContent';
import Button from '@material-ui/core/Button';
import Icon from '@material-ui/core/Icon';
import Paper from '@material-ui/core/Paper';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableContainer from '@material-ui/core/TableContainer';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import TextField from '@material-ui/core/TextField';



import DataService from "../../services/DataService";
import styles from './styles';
import TOC from '../TOC';

const Home = (props) => {
    const { classes } = props;

    console.log("================================== Home ======================================");

    const inputFile = useRef(null);

    // Component States
    const [symbol, setSymbol] = useState("");
    const [prediction, setPrediction] = useState(null);

    // Setup Component
    useEffect(() => {

    }, []);

    // Handlers
    const handleChangeSymbol = (event) => {
        setSymbol(event.target.value);
        console.log(event.target.value);
        if (event.target.value != ""){
            DataService.Predict(event.target.value)
                .then(function (response) {
                    console.log(response.data);
                    setPrediction(response.data);
                });
        }
    }

    return (
        <div className={classes.root}>
            <main className={classes.main}>
                <Container maxWidth={false} className={classes.container}>
                    <Grid container spacing={3}>
                        <Grid item xs={4}>
                            <TOC />
                        </Grid>
                        <Grid item xs={4}></Grid>
                        <Grid item xs={4}></Grid>
                    </Grid>
                </Container>
            </main>
        </div>
    );

    
};

export default withStyles(styles)(Home);