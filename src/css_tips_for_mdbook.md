# mdBookでのCSS開発Tips

<div class="meta-info">

**Create date:** 2025-07-10  
**Modified date:** 2025-07-10

</div>

mdBookでカスタムCSSを開発する際の実用的なTipsとトラブルシューティング．

## CSS反映の基本

### 設定方法
1. **CSSファイル作成**: `theme/custom.css`
2. **book.toml設定**:
   ```toml
   [output.html]
   additional-css = ["theme/custom.css"]
   ```

### ディレクトリ構造
```
mybook/
├── book.toml
├── theme/
│   └── custom.css
└── src/
    └── (mdファイル)
```

## CSS反映時の注意点

### 🔄 mdbook serve の再起動が必要
**症状**: CSSを変更しても見た目が変わらない

**解決方法**:
```bash
# mdbook serve を一度停止（Ctrl+C）
# 再起動
mdbook serve
```

**理由**: 
- mdbook serve はCSSファイルの変更を自動検知しない場合がある
- 特に新しいCSSルールや大幅な変更時に発生

### 🖥️ ブラウザキャッシュ対策

**ハードリフレッシュ**:
- **Mac**: `Cmd + Shift + R`
- **Windows**: `Ctrl + Shift + R`

## トラブルシューティング

### CSSが反映されない場合のチェックリスト

1. **book.toml設定確認**
   ```toml
   [output.html]
   additional-css = ["theme/custom.css"]  # パスが正しいか
   ```

2. **ファイル存在確認**
   ```bash
   ls theme/custom.css  # ファイルが存在するか
   ```

3. **mdbook serve の再起動**
   ```bash
   # Ctrl+C で停止
   mdbook serve
   ```

4. **ブラウザハードリフレッシュ**
   - `Cmd + Shift + R` (Mac)
   - `Ctrl + Shift + R` (Windows)

### よくある問題

#### 特定のスタイルが効かない
```css
/* !important で強制適用 */
h2 {
    margin-top: 3rem !important;
}
```

#### CSS読み込み順序の問題
```toml
# 複数CSSファイルの場合は順序に注意
[output.html]
additional-css = [
    "theme/base.css",    # 先に読み込まれる
    "theme/custom.css"   # 後に読み込まれる（優先される）
]
```

#### キャッシュ対策
```toml
# バージョン番号でキャッシュバスティング
[output.html]
additional-css = ["theme/custom.css?v=2"]
```

## 開発効率化Tips

### CSS変更の確認手順
1. CSSファイルを編集
2. `mdbook serve` を再起動
3. ブラウザでハードリフレッシュ
4. 開発者ツールで確認

### デバッグ方法
```css
/* 一時的な背景色でエリア確認 */
h2 {
    background-color: red !important; /* デバッグ用 */
}
```

```css
/* 2025-07-09: H2見出しの上余白を増加 */
h2 {
    margin-top: 3rem; /* 2rem から変更 */
}
```

[<i class="fa fa-arrow-left"></i> Home](./)
