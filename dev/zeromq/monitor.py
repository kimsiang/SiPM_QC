#!/bin/bash

until slow_control_server.py; do
    echo "slow_control_server.py' crashed with exit code $?. Restarting..." >&2
        sleep 1
        done
