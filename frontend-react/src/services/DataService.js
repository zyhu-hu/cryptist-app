import { BASE_API_URL } from "./Common";

const axios = require('axios');

const DataService = {
    Init: function () {
        // Any application initialization logic comes here
    },
    //GetLeaderboard: async function () {
    //    return await axios.get(BASE_API_URL + "/leaderboard");
    //},
    //GetCurrentmodel: async function () {
    //    return await axios.get(BASE_API_URL + "/best_model");
    //},
    // Predict: async function (formData) {
    //     return await axios.post(BASE_API_URL + "/predict", formData, {
    //         headers: {
    //             'Content-Type': 'multipart/form-data'
    //         }
    //     });
    // },
    Predict: async function (symbol) {
        return await axios.get(BASE_API_URL + "/predict_withtime/"+symbol);
    },
    Agent: async function (array) {
        return await axios.post(BASE_API_URL + "/agent", array);
    },
}

export default DataService;