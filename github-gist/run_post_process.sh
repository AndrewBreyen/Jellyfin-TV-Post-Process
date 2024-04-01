#!/bin/sh
exec > "/path/to/logging/dir/logs/$(date +"%Y-%m-%d_%H-%M-%S")-run_post_process-sh.log" 2>&1
echo $1
/usr/local/bin/python3 /path/to/record_post_process.py "$1"