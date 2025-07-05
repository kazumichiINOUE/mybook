#!/bin/bash
set -e  # エラーで即終了

GREEN='\e[32m'
RESET='\e[0m'

echo -e "${GREEN}🔧 ビルド中...${RESET}"
mdbook build

echo -e "${GREEN}📦 book/ を docs/ にコピー中...${RESET}"
rm -rf docs
mkdir -p docs
cp -r book/* docs/

echo -e "${GREEN}📤 Git にコミット＆プッシュします...${RESET}"
git add .
git commit -m "update"
git push origin main

echo -e "${GREEN}✅ 完了しました！${RESET}"
