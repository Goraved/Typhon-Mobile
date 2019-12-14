#!/usr/bin/env bash

pip3 install virtualenv
if [[ ! -f requirements.txt ]]; then
    cd ..
fi
virtualenv -p python3 venv
source venv/bin/activate
pip3 install -r requirements.txt