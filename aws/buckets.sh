#!/usr/bin/env bash
set -x
awslocal s3api create-bucket --bucket innotwitter
set +x