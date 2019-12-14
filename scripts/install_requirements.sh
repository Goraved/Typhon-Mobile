#!/usr/bin/env bash

if [[ ! -f requirements.txt ]]; then
    cd ..
fi
source venv/bin/activate
pip3 install --upgrade pip
pip3 install -r requirements.txt
deactivate