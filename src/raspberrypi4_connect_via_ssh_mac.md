# RaspberryPi4とType-Cケーブル経由でSSH接続（Mac編）

<div class="meta-info">

**Create date:** 2025-07-11  
**Modified date:** 2025-07-11

</div>

## 前提

MacとRaspberryPi4をType-Cケーブルで接続し，
電源供給をしつつSSH接続する手順を記録する．

## RaspberryPi4の設定

```admonish info
RaspberryPi4のターミナルで実行する
```

### dhcpcdのインストールと設定

1. **リポジトリ更新**
   ```bash
   sudo apt-get update
   ```

2. **dhcpcd5のインストール**
   ```bash
   sudo apt-get install dhcpcd5
   ```

3. **サービス状態確認**
   ```bash
   sudo systemctl status dhcpcd
   ```
   
   停止している場合は起動：
   ```bash
   sudo systemctl start dhcpcd
   sudo systemctl enable dhcpcd
   ```

4. **USB Ethernet設定**
   `/etc/dhcpcd.conf`に以下を追加：
   ```bash
   interface usb0
   static ip_address=192.168.7.2/24
   ```

## Mac側の設定

```admonish info
Macで実行する
```

### ネットワーク設定

1. **Type-Cケーブルで接続**
   RaspberryPi4とMacをUSB-Cケーブルで接続する．

2. **システム環境設定でネットワーク設定**
   - 「システム環境設定」→「ネットワーク」を開く
   - 「RNDIS/Ethernet Gadget」インターフェースを選択

3. **静的IP設定**
   - **Configure IPv4**: Manually
   - **IP Address**: `192.168.7.1`
   - **Subnet Mask**: `255.255.255.0`
   - **Router**: 空白
   - 「適用」をクリック

### SSH接続テスト

```bash
ssh pi@192.168.7.2
```

```admonish warning title="トラブルシューティング"
接続できない場合はケーブル接続とネットワーク設定を再確認する．
```
