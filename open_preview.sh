#!/bin/bash

# mdBook プレビューを開くスクリプト
# 使用方法: ./open_preview.sh filename.md
# または: ./open_preview.sh (現在のディレクトリの.mdファイルを自動検出)

# mdbook serve のデフォルトURL
MDBOOK_URL="http://localhost:3000"

# 引数がある場合はそのファイルを使用
if [ $# -eq 1 ]; then
    FILENAME=$(basename "$1" .md)
    echo "Opening: $1"
else
    # 引数がない場合、現在のディレクトリの.mdファイルを探す
    MD_FILES=(*.md)
    if [ ${#MD_FILES[@]} -eq 1 ] && [ -f "${MD_FILES[0]}" ]; then
        FILENAME=$(basename "${MD_FILES[0]}" .md)
        echo "Auto-detected: ${MD_FILES[0]}"
    else
        echo "Usage: $0 [filename.md]"
        echo "Or run from directory with single .md file"
        exit 1
    fi
fi

# URLを構築
URL="${MDBOOK_URL}/${FILENAME}.html"

# ブラウザで開く
echo "Opening: $URL"
open "$URL"