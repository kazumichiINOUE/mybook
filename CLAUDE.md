# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## プロジェクト概要

このリポジトリは mdBook を使用した日本語のドキュメンテーションプロジェクトです。mdBookのさまざまな機能を試すための練習用のブックとなっています。

## 主要なコマンド

### ビルド
```bash
mdbook build
```
- `book/` ディレクトリに HTML ファイルが生成される
- 自動的にサイトが書き出される

### 開発サーバー
```bash
mdbook serve
```
- ローカルで開発サーバーが起動（通常 http://localhost:3000）
- ファイル変更を監視し、自動的にリビルドされる

### ファイル監視
```bash
mdbook watch
```
- ファイル変更を監視し、変更があれば自動的にリビルドする
- サーバーは起動しない

### テスト
```bash
mdbook test
```
- ドキュメント内のRustコードサンプルのコンパイルをテストする

### 自動デプロイ
```bash
./deploy.sh
```
- ビルドからGitHub Pagesへのデプロイまでを自動化するスクリプト
- book/ を docs/ にコピーし、コミット&プッシュまで実行

## ディレクトリ構造

- `book.toml` - mdBookの設定ファイル
- `src/` - マークダウンファイルの配置場所
  - `SUMMARY.md` - ブックの目次構成
  - `README.md` - イントロダクション
  - `images/` - 画像・動画ファイル
  - `nested/` - ネストしたチャプター
- `book/` - ビルド時に生成される HTML ファイル（gitignoreされている）
- `docs/` - GitHub Pages用の公開ディレクトリ（book/のコピー）
- `deploy.sh` - 自動デプロイスクリプト

## 特徴的な機能

### ファイル埋め込み機能
- `{{#include path/to/file}}` でファイル内容を埋め込み可能
- 行範囲指定やコードブロック表示に対応

### Playground機能
- Rustコードの実行・編集・コピーが可能
- `book.toml`でplaygroundの設定を管理

### 数式サポート
- MathJaxを使った数式表示が有効

## GitHub Pages設定

- `docs/` フォルダをGitHub Pagesのソースに設定
- `deploy.sh` でビルドからデプロイまでを自動化
- メインブランチで運用

## 注意点

- `book/` ディレクトリは自動生成されるため、直接編集しない
- 公開用ファイルは `docs/` に配置される
- デプロイ前に変更点の確認が行われる

## メタ情報フォーマット

### 記事ヘッダーの統一形式
すべての記事に以下のメタ情報を追加する：

```html
<div class="meta-info">

**Create date:** YYYY-MM-DD  
**Modified date:** YYYY-MM-DD

</div>
```

- タイトル直下に配置
- `.meta-info`クラスによるCSSスタイリング適用
- 日付形式：YYYY-MM-DD（ISO 8601準拠）

## README.md目次管理規則

### SUMMARY.mdとREADME.mdの同期
README.mdの目次はSUMMARY.mdの構造と一致させる：

1. **構造の一致**
   - SUMMARY.mdのセクション構造をREADME.mdに反映
   - セクション名は完全に一致させる（例：「講義ノート」）
   - 階層レベルも同一にする

2. **記述の簡潔化**
   - README.mdでは余分な説明文を削除
   - リンクテキストのみを記載（例：`[nvimでカーソルジャンプ](nvim_cursor_jump.md)`）
   - 「- 説明文」形式の補足は基本的に削除

3. **更新タイミング**
   - SUMMARY.mdを変更した際は必ずREADME.mdも更新
   - 新規記事追加時は両方のファイルで同期確認
   - コメントアウト項目はREADME.mdには含めない

### 目次構造テンプレート
```markdown
## 目次

### セクション名
- [記事タイトル](リンク)
  - [サブ記事](サブリンク)
```

## 用語統一規則

### 技術系文書での表記
- **ハンダ**：「半田」ではなく「ハンダ」で統一
- **ハンダ付け**：「半田付け」ではなく「ハンダ付け」で統一
- **センサー**：「センサ」ではなく「センサー」で統一（長音符付き）

## セキュリティ方針

### 公開範囲の管理
- **進捗記録ファイル（PROGRESS.md等）はSUMMARY.mdに追加しない**
- 内部作業記録、プロジェクト管理ファイルは公開対象外
- 公開可否が不明な場合は事前に確認する
- mdファイルであっても内部用途のものは非公開とする