#!/usr/bin/env python3

import json, os, re, subprocess, sys, tempfile
import telegram

# Usage: ./upload_moosia.py <tg_token> <tg_chat_id> %f %n

tg_token = sys.argv[1]
tg_chat_id = int(sys.argv[2])
file_name = sys.argv[3]

if sys.argv[4] == "32":  # FTYPE_MPEG_TIMELAPSE
    timelapse = True
elif sys.argv[4] == "16":  # FTYPE_MPEG_MOTION
    timelapse = False
else:
    exit(1)

tmp = tempfile.TemporaryDirectory(prefix="moosia-uploader-")

# Extract a sane filename
vid_name = os.path.splitext(os.path.basename(file_name))[0]
vid_name = re.sub("[^0-9a-zA-Z_-]", "", vid_name)

# Convert to get better compression
subprocess.run(
    args=[
        "ffmpeg",
        "-y",
        "-loglevel",
        "error",
        "-i",
        file_name,
        "-c:v",
        "libx265",
        f"{tmp.name}/{vid_name}.mp4",
    ],
    check=True,
)

# Generate thumbnail
subprocess.run(
    check=True,
    args=[
        "ffmpeg",
        "-y",
        "-loglevel",
        "error",
        "-i",
        f"{tmp.name}/{vid_name}.mp4",
        "-vf",
        "thumbnail,scale=w=320:h=320:force_original_aspect_ratio=decrease",
        "-frames:v",
        "1",
        f"{tmp.name}/thumb.jpg",
    ],
)

# Read some metadata
metadata = json.loads(
    subprocess.run(
        check=True,
        stdout=subprocess.PIPE,
        args=[
            "ffprobe",
            "-v",
            "error",
            "-print_format",
            "json",
            "-show_streams",
            "-select_streams",
            "v:0",
            f"{tmp.name}/{vid_name}.mp4",
        ],
    ).stdout
)["streams"][0]

# Upload
tg = telegram.Bot(tg_token)
tg.send_video(
    chat_id=tg_chat_id,
    caption="#timelapse" if timelapse else None,
    video=open(f"{tmp.name}/{vid_name}.mp4", "rb"),
    thumb=open(f"{tmp.name}/thumb.jpg", "rb"),
    duration=round(float(metadata["duration"])),
    width=int(metadata["width"]),
    height=int(metadata["height"]),
    supports_streaming=True,
)
