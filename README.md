# Pybot

## About the project

- The project started as an experiment, whether I can automate a trading strategy using Python.
- This was the first pet project I started after 3 months of programming. Moreover, this was the first app that I deployed on a Linode server and sucessfully maintained for months. At this time I had no knowledge about web protocols, nor CLI editors to maintain my code. Thus, at the beginning I made several meaningless commits where I edited configuration variables after deployment.

- **Pybot** is a cryptocurrency trading bot that uses the Binance exchange to fetch historic price data from its **REST** **API**. Once the historic data is processed, it has access to **real-time** market data using **websockets**. The strategy is executed by triggering pre-defined conditions based on the incoming data feed. Once again sending request to Bnance **REST API** the orders executes instantaneously. 

## Motivation

- passion for financial markets
- practical, project oriented learning
- challenge myself 
- after months of offline scripting I wanted to experiment with web related technologies
- integrate an SDK into my project

## Technologies

- **Python** as a base language
- **Websocket API** for real-time datafeed
- **REST API** for historic data and order execution
- **Bash script** to install dependencies 

## Features

- **Binance SDK** to handle websocket and REST API endpoints
- **TA-lib** python library for technical analysis indicators
- **Logging** executed trades in CSV files
- **Customizable** strategy parameters by constant variables
- **Multiple time frame** analysis
- **USD/COIN** margined futures trading

### Disclaimer
- I created this program for educational purposes only. Binance only allows real money trading. This strategy is just a template. The current configuration is not profitable, nor have any edge on the market.
- However, due to the nature of futures trading it is possible to experiment with low balance such as $1.

## Installation and usage of the program

*The bot and the init script have been created in Linux Ubuntu 20.04 LTS environment.*
- API key and secret can only be requested from Binance, thus having an active Binance account is a requirement to start the bot.
- writing the API key and API secret to config.py
- Running the compile script in working directory by:
    - bash compile.sh

    - bash start.sh
- Executed trades can be reviewd in **./cache** folder

