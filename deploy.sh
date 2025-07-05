#!/bin/bash
set -e  # エラーで即終了

# 色設定
GREEN=$'\e[32m'
YELLOW=$'\e[33m'
RESET=$'\e[0m'

echo -e "${GREEN}🔧 ビルド中...${RESET}"
mdbook build

echo -e "${GREEN}📦 book/ を docs/ にコピー中...${RESET}"
rm -rf docs
mkdir -p docs
cp -r book/* docs/

# 変更がない場合のハンドリング
if git diff --quiet && git diff --staged --quiet; then
    echo -e "${YELLOW}📋 変更がありません。スキップします。${RESET}"
    exit 0
fi

echo -e "${GREEN}📤 Git にコミット＆プッシュします...${RESET}"
git add .

# 動的なコミットメッセージ生成
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
git commit -m "Update documentation - ${TIMESTAMP}"

git push origin main

echo -e "${GREEN}✅ 完了しました！${RESET}"
