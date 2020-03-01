#!/usr/bin/env python3

import sys, tempfile, telegram

# ./upload.py <chat_id> %f %n

chat_id = int(sys.argv[1])
file_name = sys.argv[2]
file_type = sys.argv[3]

if sys.argv[3] == "32": # FTYPE_MPEG_TIMELAPSE
    timelapse = True
elif sys.argv[3] == "16": # FTYPE_MPEG_MOTION
    timelapse = False
else:
    exit(1)

tmp = tempfile.TemporaryDirectory(prefix="moosia-uploader-")

tg = telegram.Bot("�")

#["ffmpeg", "-y", "-loglevel", "error", "-i", file_name, "-c:v", "libx265", "/full.mp4"]

print(tmp)

#tg.send_message(chat_id, "test")
