#!/usr/bin/env bash

PYTHON=2.7.12
NODE=6.9.1

echo "Installing Dependencies"
sudo apt-get -qq update
sudo apt-get -qq install -y libssl-dev libsqlite3-dev

echo "Installing Python"
cd ~
wget -q https://www.python.org/ftp/python/$PYTHON/Python-$PYTHON.tar.xz
tar -xJf Python-$PYTHON.tar.xz
cd Python-$PYTHON
./configure
sudo make
sudo make altinstall

echo "Installing Pip"
wget -q https://bootstrap.pypa.io/get-pip.py
sudo python2.7 get-pip.py

#echo "Installing virtualenv"
#sudo apt-get -qq install -y python-virtualenv

echo "Installing Node.js"
cd ~
wget -q https://nodejs.org/dist/v$NODE/node-v$NODE-linux-x64.tar.xz
sudo tar -C /usr/local --strip-components 1 -xJf node-v$NODE-linux-x64.tar.xz

echo "Installing Quasar cli"
sudo npm -q install -g quasar-cli

# PhantomJS dependency on this box
#echo "Installing fontconfig"
#sudo apt-get -qq update
#sudo apt-get -qq install -y libfontconfig

echo "Cleaning Up"
rm Python-$PYTHON.tar.xz
rm -rf Python-$PYTHON
rm node-v$NODE-linux-x64.tar.xz
