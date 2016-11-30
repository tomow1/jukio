#!/usr/bin/env bash

#virtualenv venv
#. venv/bin/activate
#python get-pip.py
#rm get-pip.py
#pip -q install pip-tools

echo "Provisioning Complete"
echo "Node.js $(node -v)"
echo "npm $(npm -v)"
python2.7 --version
pip --version

#deactivate
