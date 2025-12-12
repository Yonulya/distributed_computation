#!/usr/bin/env bash
# USAGE: ./start_worker.sh tcp://<MASTER-IP>:8786

if [ "$#" -lt 1 ]; then
  echo "Usage: $0 <scheduler-address>"
  exit 1
fi

SCHED=$1
# Tune --nthreads and --memory-limit to your worker machine
dask worker $SCHED --nthreads 4 --memory-limit 8GB