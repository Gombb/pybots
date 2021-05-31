#!/bin/bash

sudo apt-get update
sudo apt -y dist-upgrade
sudo apt -y install build-essential
sudo apt-get update
sudo apt -y install python3-pip
sudo apt -y install screen

wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz
tar -xzf ta-lib-0.4.0-src.tar.gz
cd ta-lib
sudo ./configure
sudo make
sudo make install
pip3 install ta-lib
export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH
pip3 install websocket-client
pip3 install apscheduler

sudo git clone https://github.com/Binance-docs/Binance_Futures_python.git
cd Binance_Futures_python
sudo python3 setup.py install

