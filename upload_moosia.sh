#!/usr/bin/env bash

set -eE

[ "$1" ]

tg_token="�"
tg_chat_id="�"

tg_curl() { curl "https://api.telegram.org/bot$tg_token/$@"; echo; }
trap 'tg_curl "sendMessage?chat_id=$tg_chat_id&text=Something%20wrong"' ERR

tmp=$(mktemp --directory --tmpdir moosia_uploader_XXXXX)
trap 'rm -rvf "$tmp"' EXIT

# Extract a sane filename
vid_name=${1##*/}
vid_name=${vid_name%%.*}
vid_name=${vid_name//[!0-9a-zA-Z_-]/}

# Convert to get better compression
ffmpeg -y -loglevel error -i "$1" -c:v libx265 "$tmp/full.mp4"

# Generate thumbnail
ffmpeg -y -loglevel error -i "$tmp/full.mp4" \
    -vf "thumbnail,scale=w=320:h=320:force_original_aspect_ratio=decrease" \
    -frames:v 1 "$tmp/thumb.jpg"

# Read some metadata
IFS=, read width height duration < <(
    ffprobe -v error -select_streams v:0 \
        -show_entries stream=width,height,duration -of csv=p=0 \
        "$tmp/full.mp4")

# Upload
tg_curl \
    "sendVideo?chat_id=$tg_chat_id&width=$width&height=$height&duration=$duration&supports_streaming=True" \
    -F "video=@$tmp/full.mp4;filename=Moosia_$vid_name.mp4" \
    -F "thumb=@$tmp/thumb.jpg"
