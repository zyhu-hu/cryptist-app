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
import { TimeSeries } from "pondjs";

import {
    Charts,
    ChartContainer,
    ChartRow,
    YAxis,
    LineChart,
    Baseline,
    Resizable
} from "react-timeseries-charts";

const Forecast = (props) => {
    const { classes } = props;


    console.log("================================== Forecast ======================================");
    var seriestmp = new TimeSeries({
        name: "BTC",
        columns: ["time", "value"],
        points: [[1400000000, 1400], [1400000000, 1400], [1400000000, 1400], [1400000000, 1400], [1400000000, 1400]]
        });

    // Component States
    const [symbol, setSymbol] = useState("");
    const [prediction, setPrediction] = useState(null);
    // const [points, setPoint] = useState(null);
    const [series, setSeries] = useState(seriestmp);

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
                    var pointstmp = response.data.prediction

                    var series0 = new TimeSeries({
                        name: "USD_vs_EURO",
                        columns: ["time", "value"],
                        points: pointstmp
                        // points: [[1400000000, 1400], [1400000000, 1400], [1400000000, 1400], [1400000000, 1400], [1400000000, 1400]]
                    });
                    setSeries(series0);
                });
        }
    }

   // var series = new TimeSeries({
   //     name: "USD_vs_EURO",
   //     columns: ["time", "value"],
   //     points: [[],[]]
  // });

    const style = {
        value: {
            stroke: "#a02c2c",
            opacity: 0.2
        }
    };

    const baselineStyle = {
        line: {
            stroke: "steelblue",
            strokeWidth: 1,
            opacity: 0.4,
            strokeDasharray: "none"
        },
        label: {
            fill: "steelblue"
        }
    };

    const baselineStyleLite = {
        line: {
            stroke: "steelblue",
            strokeWidth: 1,
            opacity: 0.5
        },
        label: {
            fill: "steelblue"
        }
    };

    const baselineStyleExtraLite = {
        line: {
            stroke: "steelblue",
            strokeWidth: 1,
            opacity: 0.2,
            strokeDasharray: "1,1"
        },
        label: {
            fill: "steelblue"
        }
    };

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
                            <Typography gutterBottom align='center'>
                                {prediction.asset}
                            </Typography>
                            <Typography gutterBottom align='center'>
                                {"price for next 5 time steps: " + prediction.prediction[0] + ", " + prediction.prediction[1] + ", " + prediction.prediction[2] + ", " + prediction.prediction[3] + ", " + prediction.prediction[4]}
                            </Typography>
                            <Resizable>
                                <ChartContainer
                                    title="BTC price (USD)"
                                    titleStyle={{ fill: "#555", fontWeight: 500 }}
                                    timeRange={series.range()}
                                    format="%b '%y"
                                    timeAxisTickCount={5}
                                >
                                    <ChartRow height="150">
                                        <YAxis
                                            id="price"
                                            label="Price ($)"
                                            min={series.min()}
                                            max={series.max()}
                                            width="60"
                                            format="$,.2f"
                                        />
                                        <Charts>
                                            <LineChart axis="price" series={series} style={style} />
                                            <Baseline
                                                axis="price"
                                                style={baselineStyleLite}
                                                value={series.max()}
                                                label="Max"
                                                position="right"
                                            />
                                            <Baseline
                                                axis="price"
                                                style={baselineStyleLite}
                                                value={series.min()}
                                                label="Min"
                                                position="right"
                                            />
                                            <Baseline
                                                axis="price"
                                                style={baselineStyleExtraLite}
                                                value={series.avg() - series.stdev()}
                                            />
                                            <Baseline
                                                axis="price"
                                                style={baselineStyleExtraLite}
                                                value={series.avg() + series.stdev()}
                                            />
                                            <Baseline
                                                axis="price"
                                                style={baselineStyle}
                                                value={series.avg()}
                                                label="Avg"
                                                position="right"
                                            />
                                        </Charts>
                                    </ChartRow>
                                </ChartContainer>
                            </Resizable>
                        </div>
                    }

                </Container>
            </main>
        </div>
    );
};

export default withStyles(styles)(Forecast);