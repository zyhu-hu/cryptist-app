import pandas as pd
import numpy as np
import random
from collections import deque


import gym

from tensorflow.keras import Model, Sequential, Input
from tensorflow.keras.layers import Dense, Embedding, Reshape
from tensorflow.keras.optimizers import Adam
import tensorflow.keras as keras

from google.cloud import storage
from google.oauth2 import service_account
import json


trading_instrument_idx = 48   # bitcoin binance = 48, etheruem binance = 66
ask1_idx = 0
bid1_idx = 5
trading_fees = 0.0001

class TradingEnv(gym.Env):
  def __init__(self):
    self.action_space = np.arange(-10, 10)

  def reset(self):
    # price features of all assets over past time steps
    self.x = np.random.uniform(size=(127, 10, 23))
    self.share = 0                                  # current share of bitcoin
    self.balance = 1000000                         # current cash
    # current state
    return np.concatenate((self.x.reshape(-1), [self.share/20], [self.balance/1000000])).reshape((1, -1))

  def step(self, action):
    new_share = self.share + action           # new share

    temp = np.concatenate(
        (self.x[:, :, :20]*(max-min) + min, self.x[:, :, 20:]), axis=2)

    # new balance after trading action (including trading fees)
    if action > 0:
      new_balance = self.balance - action * \
          temp[trading_instrument_idx, -1, ask1_idx]*(1+trading_fees)
    elif action < 0:
      new_balance = self.balance - action * \
          temp[trading_instrument_idx, -1, bid1_idx]*(1-trading_fees)
    else:
      new_balance = self.balance

    self.x = predictive_model(self.x)         # new self.x
    temp = np.concatenate(
        (self.x[:, :, :20]*(max-min) + min, self.x[:, :, 20:]), axis=2)

    next_state = np.concatenate(
        (self.x.reshape(-1), [self.share/20], [self.balance/1000000])).reshape((1, -1))
    reward = (new_balance + new_share*(temp[trading_instrument_idx, -1, ask1_idx]+temp[trading_instrument_idx, -1, bid1_idx])/2) - (
        self.balance + self.share*(temp[trading_instrument_idx, -2, ask1_idx]+temp[trading_instrument_idx, -2, bid1_idx])/2)  # change of net worth

    if (new_balance < 0) or (new_share < 0):    # disallow negative balance or negative share
      reward = -1e15
    terminated = False
    info = {}

    return next_state, reward, terminated, info


def transform(x):
  detrended_x = np.concatenate(
      (np.diff(x[:, :, :10], axis=1), x[:, 1:, 10:]), axis=2)
  return detrended_x


def predictive_model(x):
  """
  predictive model of our choice
  input = price features of all assets over past 10 time steps (127, 10, 23)
  output = new price features with (127, 10, 23)
  """
  loaded = keras.models.load_model(
      "/persistent/experiments/view_instrument_37_bid_and_ask")

  detrended_x = transform(x)
  y = loaded.predict(detrended_x)
  p = x[:, -1:, [ask1_idx, bid1_idx]] + y[:, 0:1, :]

  temp1 = np.copy(x[:, 1:, :])
  temp2 = np.copy(x[:, -1:, :])
  temp2[:, :, [ask1_idx, bid1_idx]] = p

  return np.concatenate((temp1, temp2), axis=1)


class Agent:
    def __init__(self, enviroment, optimizer):

        # Initialize atributes
        self._action_size = enviroment.action_space.shape[0]
        self._optimizer = optimizer

        self.expirience_replay = deque(maxlen=2000)

        # Initialize discount and exploration rate
        self.gamma = 0.6
        self.epsilon = 0.3

        # Build networks
        self.q_network = self._build_compile_model()
        self.target_network = self._build_compile_model()
        self.alighn_target_model()

    def store(self, state, action, reward, next_state, terminated):
        self.expirience_replay.append(
            (state, action, reward, next_state, terminated))

    def _build_compile_model(self):
        model = Sequential()
        model.add(Input(shape=(127*10*23+2,)))
        model.add(Dense(15, activation='relu'))
        #model.add(Dense(30, activation='relu'))
        model.add(Dense(self._action_size, activation='linear'))

        model.compile(loss='mse', optimizer=self._optimizer)
        return model

    def alighn_target_model(self):
        self.target_network.set_weights(self.q_network.get_weights())

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return np.random.choice(enviroment.action_space)

        return self.get_optimal_action(state)

    def get_optimal_action(self, state):
        np.random.seed(0)
        q_values = self.q_network.predict(state)
        if np.any(np.isnan(q_values[0])):
          share = state[0, -2]*20
          balance = state[0, -1]*1000000
          interval = np.arange(
              np.max([-int(share), -10]), np.min([int(balance/50000), 10]))
          return np.random.choice(interval)
        return np.argmax(q_values[0])

    def retrain(self, batch_size):
        minibatch = random.sample(self.expirience_replay, batch_size)

        for state, action, reward, next_state, terminated in minibatch:

            target = self.q_network.predict(state)

            if terminated:
                target[0][action] = reward
            else:
                t = self.target_network.predict(next_state)
                target[0][action] = reward + self.gamma * np.amax(t)

            self.q_network.fit(state, target, epochs=1, verbose=0)

def create_agent():
    enviroment = TradingEnv()
    optimizer = Adam(learning_rate=0.1)
    agent = Agent(enviroment, optimizer)
    agent.q_network = keras.models.load_model(
        "/persistent/experiments/q_model.h5")
    agent.alighn_target_model()
    return agent

def trading_action(agent, x, share, balance,total):
    max = pd.read_csv(
        '/persistent/experiments/max.csv').values[:, 1].astype('float')
    min = pd.read_csv(
        '/persistent/experiments/min.csv').values[:, 1].astype('float')
    """
    Define current state here!
    x = price feature array (127, 10, 23)
    share = current # of shares of trading instrument
    balance = current cash left
    """
    temp = np.concatenate(
        (x[:, :, :20]*(max-min) + min, x[:, :, 20:]), axis=2)


    state = np.concatenate(
        (x.reshape(-1), [share/20], [balance/1000000])).reshape((1, -1))
    optimal_action = agent.get_optimal_action(state)
    share_new = share + optimal_action
    if optimal_action > 0:
      new_balance = balance - optimal_action * \
          temp[trading_instrument_idx, -1, ask1_idx]*(1+trading_fees)
    elif optimal_action < 0:
      new_balance = balance - optimal_action * \
          temp[trading_instrument_idx, -1, bid1_idx]*(1-trading_fees)
    else:
      new_balance = balance
    total = new_balance + share_new*0.5 * \
        (temp[trading_instrument_idx, -1, ask1_idx] +
         temp[trading_instrument_idx, -1, bid1_idx])

    return round(total, 2), round(new_balance, 2), share_new
