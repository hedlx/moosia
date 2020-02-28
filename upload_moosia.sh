#!/usr/bin/env bash

set -eE

[ "$1" ]

tg_token="�"
tg_chat_id="�"

tg_curl() { curl "https://api.telegram.org/bot$tg_token/$@"; echo; }
trap 'tg_curl "sendMessage?chat_id=$tg_chat_id&text=Something%20wrong"' ERR

tmp_vid=$(mktemp "/tmp/tg_upload_XXXX.mp4")
trap 'rm -vf "$tmp_vid"' EXIT

ffmpeg -y -loglevel error -i "$1" "$tmp_vid"
tg_curl "sendVideo?chat_id=$tg_chat_id" -F "video=@$tmp_vid"
