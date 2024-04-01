#!/bin/sh
if [ $# -eq 0 ]
  then
    echo "No arguments supplied, exiting..."
    echo "Usage: /Users/Shared/Scripts/run_post_processor.sh \"/path/to/file.ts\""
    echo
    exit
fi
exec > "/Users/Shared/Scripts/logs/$(date +"%Y-%m-%d_%H-%M-%S")-run_post_process-sh.log" 2>&1
echo $1
/usr/local/bin/python3 /Users/Shared/Scripts/record_post_process.py "$1"