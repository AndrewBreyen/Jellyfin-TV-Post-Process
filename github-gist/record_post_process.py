"""Post-Process Files"""
# !/usr/bin/python3

import logging
import os
import sys
import time
from pathlib import Path
from time import strftime

LOGFILE = "/path/to/logging/directory/logs/{}-record_process-py.log".format(
    strftime("%Y-%m-%d_%H-%M-%S")
)
logging.basicConfig(
    filename=LOGFILE, format="%(levelname)s:%(message)s", level=logging.INFO
)


def main():
    """main method"""

    # check for args
    if len(sys.argv) == 1:
        raise TypeError(
            f"Expected 2 arguments, got {len(sys.argv)}.\nArgs recieved: {str(sys.argv)}"
        )

    # /path/to/series/show/season/vid.ext
    file_path = sys.argv[1]

    # vid
    basename = os.path.basename(file_path).split(".")[0]

    # vid.ext
    file_name = os.path.basename(file_path)

    # /path/to/series/show/season/
    vid_dir = str(Path(file_path).parents[0])

    # vid.mp4
    out_file = basename + ".mp4"

    # /path/to/series/show/season/vid.mp4
    out_path = vid_dir + "/" + out_file

    # /path/to/OLDFILES
    move_to = str(Path(file_path).parents[2]) + "/OLDFILES"

    # /path/to/OLDFILES/BAK_vid.ext
    bak_file_path = move_to + "/BAK_" + file_name

    logging.info("Starting transcode! \n Filename: %s", basename)

    ##############################
    # FFMPEG COMMAND + EXECUTION #
    ##############################

    # command to run in a shell (ensure that the full path to ffmpeg is specified: [result of which ffmpeg])
    command = (
        '/usr/local/bin/ffmpeg -i "'
        + file_path
        + '" -vcodec h264_videotoolbox -acodec copy -b:v 3000k "'
        + out_path
        + '"'
    )

    logging.debug("FFMPEG command: %s", command)

    # record start time
    start_time = time.time()

    # try to run ffmpeg 
    try:
        os.system(command)
    except Exception as exception:
        logging.exception(exception)
        raise exception

    # record end time and compute total time (rounded)
    total_time = round(time.time() - start_time, 3)

    logging.info("DONE! Transcode of %s completed in %d seconds!", basename, total_time)

    #################################
    # MOVE NONTRANSCODED OUT OF DIR #
    #################################

    # check if directory OLDFILES exists up two levels, if it does not, create it
    if not os.path.exists(move_to):
        logging.info("move_to_path does not exist, will create...")
        os.makedirs(move_to)

    # attempt to move and rename old non-transcoded file out of its current location so Jellyfin does not see it
    try:
        os.rename(file_path, bak_file_path)
        logging.info("Non-transcoded file moved and renamed to %s", bak_file_path)
    except OSError as exception:
        logging.exception(exception)
        raise exception

if __name__ == "__main__":
    main()
