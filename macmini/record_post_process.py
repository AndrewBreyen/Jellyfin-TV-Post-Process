"""Post-Process Files"""
# !/usr/bin/python3

import logging
import os
import sys
import time
from pathlib import Path
from time import strftime
from slack_sdk import WebClient
from dotenv import load_dotenv

slack_api_token = os.getenv("SLACK_API_TOKEN")

client = WebClient(token=slack_api_token)

CHANNEL = "C02U64GT5QB"

LOGFILE = "/Users/Shared/Scripts/logs/{}-record_process-py.log".format(
    strftime("%Y-%m-%d_%H-%M-%S")
)
logging.basicConfig(
    filename=LOGFILE, format="%(levelname)s:%(message)s", level=logging.INFO
)

def add_react(react, time_stamp):
    """Adds a specified reaction (react) to a slack message specified via timestamp (time_stamp)"""
    client.reactions_add(channel=CHANNEL, name=react, timestamp=time_stamp)


def remove_react(react, time_stamp):
    """Removes a specified reaction to a slack message specified via timestamp (time_stamp)"""
    client.reactions_remove(channel=CHANNEL, name=react, timestamp=time_stamp)


def send_parent_message(msg):
    """Sends a parent message with specified text (msg)"""
    return client.chat_postMessage(channel=CHANNEL, text=msg)


def send_reply_message(msg, time_stamp):
    """Sends a reply message with specified message to a parent message specified by timestamp"""
    client.chat_postMessage(channel=CHANNEL, thread_ts=time_stamp, text=msg)


def update_msg(msg, time_stamp):
    """updates a message specified by timestamp to be msg"""
    client.chat_update(channel=CHANNEL, ts=time_stamp, text=msg)


def error_ocurred(msg, time_stamp):
    """Note that an error occurred, reply to parent message with specified message (msg)"""
    client.chat_postMessage(
        channel=CHANNEL,
        thread_ts=time_stamp,
        text=f"ERROR: {msg}",
    )
    add_react("warning", time_stamp)

    logging.critical("ERROR: %s", msg)
    sys.exit()

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
    basename_int = os.path.basename(file_path).rsplit('.', 1)
    basename_int = basename_int[0].replace('.',' ')
    basename = basename_int

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

    parent = send_parent_message(f"Starting Transcode of `{basename}`")
    timestamp = parent["ts"]

    logging.info("Starting transcode! \n Filename: %s", basename)
    add_react("beachball", timestamp)

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
        remove_react("beachball", timestamp)
        send_reply_message(
            f"Error ocurred while processing `{filename}`!",
            timestamp,
        )
        error_ocurred(exception, timestamp)
        logging.exception(exception)
        raise exception

    # record end time and compute total time (rounded)
    total_time = round(time.time() - start_time, 3)
    minutes = round(total_time / 60, 2)

    # update slack message to say complete, reply with total time, and remove the beach ball loading
    remove_react("beachball", timestamp)
    update_msg(f"Transcode of `{basename}` completed! :party_parrot:", timestamp)
    send_reply_message(
        f":clock1: Completed in `{total_time}` seconds == `{minutes}` minutes!", timestamp
    )
    logging.info(
        "DONE! Transcode of %s completed in %d seconds! (%d minutes)",
        basename,
        total_time,
        minutes,
    )

    #################################
    # MOVE NONTRANSCODED OUT OF DIR #
    #################################

    # # check if directory OLDFILES exists up two levels, if it does not, create it
    # if not os.path.exists(move_to):
    #     logging.info("move_to_path does not exist, will create...")
    #     os.makedirs(move_to)

    # # attempt to move and rename old non-transcoded file out of its current location so Jellyfin does not see it
    # try:
    #     os.rename(file_path, bak_file_path)
    #     logging.info("Non-transcoded file moved and renamed to %s", bak_file_path)
    # except OSError as exception:
    #     logging.exception(exception)
    #     raise exception


    #############################
    # DELETE NONTRANSCODED FILE #
    #############################

    os.remove(file_path)
    logging.info("Deleted non-transcoded file %s", file_path)

if __name__ == "__main__":
    main()