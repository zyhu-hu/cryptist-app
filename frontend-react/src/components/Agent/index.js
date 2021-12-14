import React, { useEffect, useRef, useState } from 'react';
import { withStyles } from '@material-ui/core';
import Container from '@material-ui/core/Container';
import Typography from '@material-ui/core/Typography';
import InputLabel from '@material-ui/core/InputLabel';
import MenuItem from '@material-ui/core/MenuItem';
import FormHelperText from '@material-ui/core/FormHelperText';
import FormControl from '@material-ui/core/FormControl';
import Select from '@material-ui/core/Select';

import DataService from "../../services/DataService";
import styles from './styles';



const Agent = (props) => {
    const { classes } = props;


    console.log("================================== Agent ======================================");
    

    // Component States
    const [symbol, setSymbol] = useState("");
    const [prediction, setPrediction] = useState(null);
    // const [points, setPoint] = useState(null);
    const [intervalId, setIntervalId] = useState(0);


    // Setup Component
    useEffect(() => {

    }, []);

    // Handlers
    const handleChangeSymbol = (event) => {
        setSymbol(event.target.value);
        console.log(event.target.value);
        if (event.target.value !== "") {
            DataService.Predict(event.target.value)
                .then(function (response) {
                    console.log(response.data);
                    setPrediction(response.data);
                    
                });
        }

    }


   // var series = new TimeSeries({
   //     name: "USD_vs_EURO",
   //     columns: ["time", "value"],
   //     points: [[],[]]
  // });


    return (
        <div className={classes.root}>
            <main className={classes.main}>
                <Container maxWidth="md" className={classes.container}>
                    <Typography variant="h4">Select a Symbol</Typography>
                    <br />
                    <FormControl variant="outlined" className={classes.formControl} fullWidth={true}>
                        <InputLabel id="demo-simple-select-outlined-label">Symbol</InputLabel>
                        <Select
                            labelId="demo-simple-select-outlined-label"
                            id="demo-simple-select-outlined"
                            value={symbol}
                            onChange={handleChangeSymbol}
                            label="Symbol"
                        >
                            <MenuItem value="">
                                <em>-Select-</em>
                            </MenuItem>
                            <MenuItem value={"BINANCE:ETH_USDT.SWAP"}>Ethereum</MenuItem>
                            <MenuItem value={"BINANCE:BTC_USDT.SWAP"}>Bitcoin</MenuItem>
                        </Select>
                    </FormControl>
                    <br />
                    {prediction &&
                        <div>
                            
                        </div>
                    }

                </Container>
            </main>
        </div>
    );
};

export default withStyles(styles)(Agent);