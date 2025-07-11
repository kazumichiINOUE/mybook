# mdbookにコードやファイルの内容を埋め込む

<div class="meta-info">

**Create date:** 2025-07-05  
**Modified date:** 2025-07-05

</div>

参照: <https://rust-lang.github.io/mdBook/format/mdbook.html?highlight=include#including-files>

mdbookには，ローカルファイルを取り込む機能が提供されている．
手元にあるソースコードを，そのまま共有したい場合に重宝する．
ローカルファイルを修正すれば，そのままmdbookにも反映されるので，一貫性を保ちやすい．

## 基本
```markdown
\{{#include relative/path/to/file}}
```
これで，`relative/path/to/file`の部分を，埋め込みたいファイルへの相対パスに変えればよい．
これは，任意のファイルの中身を埋め込む方法として使えるが，ソースコードの場合，ほとんどは
コードブロックとして表示したいと思われる．以下が，コードブロックとしての使い方である．

````code
```filetype
\{{#include relative/path/to/file}}
```
````
`filetype`の部分には，埋め込むファイルの種類を書いておく．シンタックスハイライトが効く．

上の書き方で実際に使うと，以下のように埋め込まれる．

**markdown中の書き方**
````toml
```toml
\{{#include ../book.toml}}
```
````

**実際の表示**
```toml
{{#include ../book.toml::9}}
```

## 高度な使い方
### 埋め込む範囲を指定する
**指定した行だけ**
````toml
```toml
\{{#include ../book.toml:2}}
```
````
```toml
{{#include ../book.toml:2}}
```

**行の範囲指定**
````toml
```toml
\{{#include ../book.toml:2:5}}
```
````
```toml
{{#include ../book.toml:2:5}}
```

**指定した行以降**
````toml
```toml
\{{#include ../book.toml:5:}}
```
````
```toml
{{#include ../book.toml:5:}}
```

**指定した行まで**
````toml
```toml
\{{#include ../book.toml::5}}
```
````
```toml
{{#include ../book.toml::5}}
```

[<i class="fa fa-arrow-left"></i> Home](./)
