#!/bin/sh
WD="$(cd "$(dirname "$0")"; pwd -P)"
SOURCE="$WD/env/bin/activate"
MAIN="$WD/studip_scorer/__init__.py"

source "${SOURCE}"
python3 "${MAIN}"
