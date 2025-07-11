# Raspberry Pi 4でlxterminalの日本語入力問題を解決する方法

<div class="meta-info">

**Create date:** 2025-07-10  
**Modified date:** 2025-07-10

</div>

## 問題の概要

Raspberry Pi 4のLXTerminalにて，日本語入力時に母音（あ，い，う，え，お）しか入力できず，
子音を含む文字が正常に入力できない現象が発生することがあります．
`ki`のようなキー入力において，一つづつ確定されているような挙動を確認できます．

## 症状

- lxterminalで日本語入力モードにしても母音以外の文字が入力できない
- 他のアプリケーションでは正常に日本語入力ができる場合がある
- 英数字入力は正常に動作する

## 解決方法

以下の3つのコマンドを順番に実行することで解決できます．

```bash
sudo apt install fcitx5-mozc # 1. fcitx5-mozcのインストール
im-config -n fcitx5          # 2. 入力メソッドの設定変更
sudo reboot                  # 3. システムの再起動
```

設定を確実に反映させるため，システムを再起動します．
この方法により，Raspberry Pi 4でのlxterminalの日本語入力問題を解決できます．
