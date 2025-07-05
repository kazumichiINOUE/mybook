#!/bin/bash
set -e  # エラーで即終了

echo "🔧 ビルド中..."
mdbook build

echo "📦 book/ を docs/ にコピー中..."
rm -rf docs
mkdir -p docs
cp -r book/* docs/

echo "📤 Git にコミット＆プッシュします..."
git add .
git commit -m "update"
git push origin main

echo "✅ 完了しました！"
