#!/bin/bash
wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz
tar -xzf ta-lib-0.4.0-src.tar.gz
cd ta-lib/
sudo ./configure
sudo make
sudo make install
pip3 install ta-lib

git clone https://github.com/Binance-docs/Binance_Futures_python.git
cd Binance_Futures_python
python3 setup.py.install
