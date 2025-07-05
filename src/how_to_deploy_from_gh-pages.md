# gh-pagesでmdbookを公開する

`mdbook`とは，rust製のオンラインドキュメント制作ツールの名称．  
<i class="fa fa-arrow-right"></i>
[mdBook Documentation](https://rust-lang.github.io/mdBook/)

`gh-pages`とは，GitHubのリポジトリをWeb公開する，GitHubが提供している仕組み．  
<i class="fa fa-arrow-right"></i>
[What is GitHub Pages?](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages?utm_source=chatgpt.com)

## mdbookをローカルで用意する
```bash
mdbook init mybook
cd mybook
# 何かしらmybookの中を制作
mdbook build
```

## Githubで新しいリポジトリを作成する
ここでは，`mybook` というリポジトリを作成したとする．

## mybook/bookをgithubに連携させる
```bash
# 現在の場所: mdbookのルート
cd book
git init
git remote add origin https://github.com/<your-username>/mybook.git
git checkout -b gh-pages
git add .
git commit -m "deploy to GitHub Pages"
git push -f origin gh-pages
```

## GitHub Pages を有効化
GitHub のリポジトリページ → Settings → Pages に行く．
* `Source`: gh-pages ブランチを選択
* `Folder`: / (root) を選択
* 保存すると、数秒〜数分で https://\<your-username\>.github.io/mybook/ に公開される

## ページの更新
```bash
mdbook build
cd book
git add .
git commit -m "update"
git push origin gh-pages
```

> <i class="fa fa-lightbulb-o"></i> 
> このページ自体も`gh-pages`を使って公開しています．
