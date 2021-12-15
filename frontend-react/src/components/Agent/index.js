import React, { useEffect, useRef, useState } from 'react';
import { withStyles } from '@material-ui/core';
import Container from '@material-ui/core/Container';
import Typography from '@material-ui/core/Typography';
import InputLabel from '@material-ui/core/InputLabel';
import MenuItem from '@material-ui/core/MenuItem';
import FormHelperText from '@material-ui/core/FormHelperText';
import FormControl from '@material-ui/core/FormControl';
import Select from '@material-ui/core/Select';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableContainer from '@material-ui/core/TableContainer';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import DataService from "../../services/DataService";
import Paper from '@material-ui/core/Paper';
import { makeStyles } from '@material-ui/core/styles';
import styles from './styles';
import Button from '@material-ui/core/Button';


function useInterval(callback, delay) {
    const intervalRef = React.useRef();
    const callbackRef = React.useRef(callback);

    // Remember the latest callback:
    //
    // Without this, if you change the callback, when setInterval ticks again, it
    // will still call your old callback.
    //
    // If you add `callback` to useEffect's deps, it will work fine but the
    // interval will be reset.

    React.useEffect(() => {
        callbackRef.current = callback;
    }, [callback]);

    // Set up the interval:

    React.useEffect(() => {
        if (typeof delay === 'number') {
            intervalRef.current = window.setInterval(() => callbackRef.current(), delay);

            // Clear interval if the components is unmounted or the delay changes:
            return () => window.clearInterval(intervalRef.current);
        }
    }, [delay]);

    // Returns a ref to the interval ID in case you want to clear it manually:
    return intervalRef;
}

const Agent = (props) => {

    const { classes } = props;

    function createData(name, value) {
        return { name, value };
    }

    const rows_init = [
        createData('Total account value (USD)', 1000000),
        createData('Buying power (USD)', 1000000),
        createData('Asset name', null),
        createData('Asset shares', 0),
        createData('Time step', 0),
    ];


    console.log("================================== Agent ======================================");
    

    // Component States
    const [symbol, setSymbol] = useState("");
    const [prediction, setPrediction] = useState(null);
    const [rows, setRow] = useState(rows_init);
    const [intervalId, setIntervalId] = useState(0);
    // const [points, setPoint] = useState(null);



    // Setup Component
    useEffect(() => {

    }, []);

    // Handlers
    const handleChangeSymbol = (event) => {
        setSymbol(event.target.value);
        console.log(event.target.value);
        let rows_tmp = [
            createData('Total account value (USD)', rows[0].value),
            createData('Buying power (USD)', rows[1].value),
            createData('Asset name', event.target.value),
            createData('Asset shares', rows[3].value),
            createData('Time step', rows[4].value),
        ];
        setRow(rows_tmp);
    }

    const handleChangeStartTrading = () => {
        console.log('Taking action');
        DataService.Agent(rows)
            .then(function (response) {
                console.log(response.data);
                var rows_tmp1 = [
                    createData('Total account value (USD)', response.data.total),
                    createData('Buying power (USD)', response.data.power),
                    createData('Asset name', rows[2].value),
                    createData('Asset shares', response.data.shares),
                    createData('Time step', rows[4].value + 1),
                ];
                setRow(rows_tmp1);
            });
        //setIntervalId(newIntervalId);
    
    }

    const handleChangeResetTrading = () => {
        console.log('reset trading data');
        DataService.Agent(rows)
            .then(function (response) {
                console.log(response.data);
                let rows_tmp1 = [
                    createData('Total account value (USD)', 1000000),
                    createData('Buying power (USD)', 1000000),
                    createData('Asset name', symbol),
                    createData('Asset shares', 0),
                    createData('Time step', 0),
                ];
                setRow(rows_tmp1);

            });

    }

    const useStyles = makeStyles({
        table: {
            minWidth: 850,
        },
    });

    const classest = useStyles(); // for table

    const useStyles_bt = makeStyles((theme) => ({
        root: {
            '& > *': {
                margin: theme.spacing(1),
            },
        },
    }));

    const classesbt = useStyles_bt(); // for button

   // var series = new TimeSeries({
   //     name: "USD_vs_EURO",
   //     columns: ["time", "value"],
   //     points: [[],[]]
  // });


    return (
        <div className={classest.root}>
            <main className={classest.main}>
                <Container maxWidth="md" className={classest.container}>
                    <Typography variant="h4">Select a Symbol</Typography>
                    <br />
                    <FormControl variant="outlined" className={classest.formControl} fullWidth={true}>
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

                    <div className={classesbt.root}>
                        <Button onClick={handleChangeStartTrading} variant="contained" color="primary">
                            Take action
                        </Button>
                        <Button onClick={handleChangeResetTrading} variant="contained" color="secondary">
                            Reset
                        </Button>
                    </div>
                    <TableContainer component={Paper}>
                        <Table className={classest.table} aria-label="simple table">
                    
                            <TableBody>
                                {rows.map((row) => (
                                    <TableRow key={row.name}>
                                        <TableCell component="th" scope="row">
                                            {row.name}
                                        </TableCell>
                                        <TableCell align="right">{row.value}</TableCell>
                                    </TableRow>
                                ))}
                            </TableBody>
                        </Table>
                    </TableContainer>

                    {prediction &&
                        <div>
                            <Typography gutterBottom align='center'>
                                {prediction.asset}
                            </Typography>
                        </div>
                    }

                </Container>
            </main>
        </div>
    );
};

export default withStyles(styles)(Agent);