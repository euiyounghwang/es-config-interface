

#!/bin/bash
set -e

# Activate virtualenv && run serivce

SCRIPTDIR="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
cd $SCRIPTDIR

VENV=".venv"

# Python 3.11.7 with Window
if [ -d "$VENV/bin" ]; then
    source $VENV/bin/activate
else
    source $VENV/Scripts/activate
fi


# -- background
#  sudo netstat -nlp | grep :8100
# nohup $SCRIPTDIR/service-start.sh &> /dev/null &

python -m uvicorn main:app --reload --host=0.0.0.0 --port=8100 --workers 4
# poetry run uvicorn main:app --reload --host=0.0.0.0 --port=8003 --workers 4
