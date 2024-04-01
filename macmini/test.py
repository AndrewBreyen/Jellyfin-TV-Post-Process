import logging
import os
import sys
import time
from pathlib import Path
from time import strftime

# check for args
if len(sys.argv) == 1:
    raise TypeError(
        f"Expected 2 arguments, got {len(sys.argv)}.\nArgs recieved: {str(sys.argv)}"
    )
# /path/to/series/show/season/vid.ext
file_path = sys.argv[1]
print("Filepath:" + file_path)
# vid
print("BAsenameINT")
basename_int = os.path.basename(file_path).rsplit('.', 1)
print(basename_int)
basename_int = basename_int[0].replace('.',' ')

basename = basename_int
print("Basename:" + basename)
# vid.ext
file_name = os.path.basename(file_path)
print("Filename: " + file_name)
# /path/to/series/show/season/
vid_dir = str(Path(file_path).parents[0])
print("Viddir:" + vid_dir)
# vid.mp4
out_file = basename + ".mp4"
print("outfile: " + out_file)
# /path/to/series/show/season/vid.mp4
out_path = vid_dir + "/" + out_file
print("outpath: "+ out_path)
