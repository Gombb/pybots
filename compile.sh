#!/bin/bash

sudo apt-get update
sudo apt-get dist-upgrade
sudo apt-get install build-essential
sudo apt-get update
sudo apt install python3-pip
sudo apt-get install screen

wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz
tar -xzf ta-lib-0.4.0-src.tar.gz
cd ta-lib
sudo ./configure
sudo make
sudo make install
pip3 install ta-lib
pip3 install websocket-client
pip3 install apscheduler

git clone https://github.com/Binance-docs/Binance_Futures_python.git
cd Binance_Futures_python
python3 setup.py.install

