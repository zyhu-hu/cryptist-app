# cryptist-app

This is an app for a course project (AC215).

## App components

This app contains two components: Forecast and Trading-agent.

A user can choose an asset (for now, that's gonna be either Bitcoin or Ethereum).
The Forecast component will display the forecast price of the asset based on pretrained deep learning models. Below is an illustration of the Forecast component:

![image](https://user-images.githubusercontent.com/57764895/143981976-84e4add7-712d-4458-a5a9-857e2bafefa9.png)


The Trading-agent component (have not deployed yet, but it can be deployed just as the Forecast component) will simulate a AI trading agent (trained with deep reinforcement learning) and display the performence of the trading agent (a time series of the total assets or the P&L)

## App modules

The frontend module, implemented with react, serves as the web interface with users.

The api-service module is used to: 1) download prediction model and deep reinforcement learning (DRL) trading agent from the GCP bucket; 2) making prediction of asset price using available prediction models; 3) take action with the AI trading agent.

The deployment model is used to set up the app on GCP and K8s clusters.

We also have a model-training module to train the prediction model and the DRL trading agent model. This module has been developing separately for now and will be included in the repo.
