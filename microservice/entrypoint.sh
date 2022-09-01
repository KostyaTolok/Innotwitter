#!/bin/sh

set -e

echo "Starting microservice on 0.0.0.0:3000"
uvicorn main:app --reload --port 3000 --host 0.0.0.0