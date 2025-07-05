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

# コミットメッセージの入力を求める
echo -n "コミットメッセージを入力してください (空白でデフォルト): "
read -r COMMIT_MESSAGE

# タイムスタンプ生成
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

# メッセージが空の場合はデフォルトメッセージを使用
if [ -z "$COMMIT_MESSAGE" ]; then
    COMMIT_MESSAGE="Update documentation"
fi

# 最終的なコミットメッセージを表示して確認
FINAL_MESSAGE="${COMMIT_MESSAGE} - ${TIMESTAMP}"
echo -e "${YELLOW}コミットメッセージ: \"${FINAL_MESSAGE}\"${RESET}"
echo -n "このメッセージでコミットしますか？ (y/n): "
read -r CONFIRM

if [ "$CONFIRM" != "y" ] && [ "$CONFIRM" != "Y" ]; then
    echo -e "${YELLOW}❌ コミットをキャンセルしました。${RESET}"
    exit 1
fi

# タイムスタンプを追加してコミット
git commit -m "${FINAL_MESSAGE}"

git push origin main

echo -e "${GREEN}✅ 完了しました！${RESET}"
