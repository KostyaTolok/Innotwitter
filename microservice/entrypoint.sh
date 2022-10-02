#!/bin/sh

set -e

echo "Generating statistics table"
python generate_page_statistics_table.py

echo "Starting microservice on 0.0.0.0:3000"
uvicorn main:app --reload --port 3000 --host 0.0.0.0