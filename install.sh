#!/bin/bash
echo "Installing studip-scorer..."

python3 -m venv env
source env/bin/activate
pip install -r requirements.txt

echo "Installing studip-scorer finished. Please look at the log for possible errors."
