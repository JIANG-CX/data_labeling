#!/bin/bash

DIFF=`yapf -p -r -d --style='{COLUMN_LIMIT:80}' ./`
if [ ! -z "$DIFF" ]
then
    echo "yapf format check failed"
    printf -- "$DIFF"
    false
else
    echo "yapf format check succeeded"
fi
