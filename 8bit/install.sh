#!/bin/sh
# 8bit 라이브러리에 넣을 폴더를 만든다. 사용법: sh 8bit/install.sh <대상 폴더> <플레이 주소>
set -eu
source_dir=$(dirname "$0")
target_dir=$1
play_url=$2
mkdir -p "$target_dir/build" "$target_dir/docs"
cp "$source_dir/cover.webp" "$target_dir/"
cp "$source_dir"/docs/*.md "$target_dir/docs/"
sed "s|__PLAY_URL__|$play_url|g" "$source_dir/manifest.json" > "$target_dir/manifest.json"
sed "s|__PLAY_URL__|$play_url|g" "$source_dir/build/index.html" > "$target_dir/build/index.html"
