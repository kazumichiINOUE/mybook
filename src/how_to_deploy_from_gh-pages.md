# gh-pagesでmdbookを公開する

**Create date:** 2025-07-05  
**Modified date:** 2025-07-05

`mdbook`とは，rust製のオンラインドキュメント制作ツールの名称．  
<i class="fa fa-arrow-right"></i>
[mdBook Documentation](https://rust-lang.github.io/mdBook/)

`gh-pages`とは，GitHubのリポジトリをWeb公開する，GitHubが提供している仕組み．  
<i class="fa fa-arrow-right"></i>
[What is GitHub Pages?](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages?utm_source=chatgpt.com)

> <i class="fa fa-lightbulb-o"></i> 
> このページ自体も`gh-pages`を使って公開しています．


## mdbookをローカルで用意する
```bash
mdbook init mybook
cd mybook
# 最初に，公開用のディクレトリをdocsという名前で作成する
mkdir docs
```

## Githubで新しいリポジトリを作成する
ここでは，`mybook` というリポジトリを作成したとする．

## mybook/bookをgithubに連携させる
```bash
# 現在の場所: mdbookのルート
git init
echo "book" >> .gitignore
git remote add origin https://github.com/<your-username>/mybook.git
git add .
git commit -m "deploy to GitHub Pages"
git push -f origin main
```

## GitHub Pages を有効化
GitHub のリポジトリページ → Settings → Pages に行く．
* `Source`: main ブランチを選択
* `Folder`: /docs を選択
* 保存すると、数秒〜数分で *https://\<your-username\>.github.io/mybook/* に公開される

## mdbookを編集したら，ビルド・公開用ディレクトリにコピーをする
```bash
# 何かしらmybookの中を制作
mdbook build
cp -r book/* docs/
```

## ページの更新
```bash
git add .
git commit -m "update"
git push origin main
```

## シェルスクリプトで更新を自動化
以下のシェルスクリプトにより，ビルドからプッシュまでを自動化できる．
```shell, numberLines
{{#include ../deploy.sh}}
```
**使い方**
```bash
nvim deplay.sh # 上記スクリプトを作成
chmod +x deplay.h # 実行権限を付与．最初だけで良い
./deplay.h
```

[<i class="fa fa-arrow-left"></i> Home](./)
