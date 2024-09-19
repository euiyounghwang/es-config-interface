

#!/bin/bash
set -e

JAVA_HOME=~/openlogic-openjdk-11.0.23+9-linux-x64
export PATH=$JAVA_HOME/bin:$PATH
export JAVA_HOME


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

python -m uvicorn main:app --reload --host=0.0.0.0 --port=8004 --workers 1

#- https://chaechae.life/blog/fastapi-deployment-gunicorn
#gunicorn -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:8004 --workers 4
#poetry run uvicorn main:app --reload --host=0.0.0.0 --port=8004 --workers 4
