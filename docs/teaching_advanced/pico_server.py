"""
# Pico 温度・気圧・湿度計測データ送信プログラム

## 1. 概要
このプログラムは，Raspberry Pi Pico (以下，Pico) 上で動作する，
温度・気圧・湿度センサーによる計測と，その計測データをネットワーク接続したクライアントPCへ送信
するプログラムです．
計測データは，Picoに接続したOLEDディスプレイにも表示されます．
基本的には，USB電源によるスタンドアローン (PCなどには接続せず，単独で動作させる)な使い方を想定して
います．

## 2. 接続しているデバイス
- 温度・気圧・湿度センサー: BME280 (5V仕様) 1台
- OLEDディスプレイ: SSD1306 1台
- LED: 砲弾型LED 1個

## 3. 動作フロー
1) main()関数より，`start_server()` を呼び出し（実質的なメイン関数）
2) WiFi接続を確立（失敗したら停止）
3) BME280接続を確立（失敗したら停止）
4) サーバーを起動し，リクエストを待機
5) `handle_client()`にて，リクエストに対応
5-1) "led_on": led.on()
5-2) "led_off": led.off()
5-3) "get_status": response
5-4) "ping": response
5-5) "get_sensor_data": 
        bmeが初期化できている場合: response {temp, pres, hum}
        それ以外: response error
5-6) それ以外: response 

## 4. 設定項目
SSID = ユーザーにより設定
PASSWORD = ユーザーにより設定
SERVER_PORT = ユーザーにより設定 (デフォルト: 8080)
PICO_ID = XX  (各Picoで1，2，3に変更)

## 5. ライブラリ
- bme280_float.py
- ssd1306

## 6. 使用方法
`main.py`として起動する (Picoに書き込まれている場合，電源を入れれば自動でスタートする)
PCで，`multi_client.py`を起動し，リクエストを送信することでデータ収集ができるようになる．
"""
import network
import socket
import time
import machine
import json
import bme280_float as bme280

# WiFi設定
SSID = "Buffalo-9EC0"
PASSWORD = "66x6h6hjjtvbk"

# サーバー設定
SERVER_PORT = 8080

# Pico固有ID設定（各Picoで1，2，3に変更）
PICO_ID = XX

# LED設定
led = machine.Pin("LED", machine.Pin.OUT)

# BME280設定（I2C）
bme = None

def init_bme280():
    """BME280センサーの初期化"""
    global bme
    try:
        # I2C設定
        i2c_bme = machine.I2C(0, scl=machine.Pin(17), sda=machine.Pin(16), freq=100000)
        devices = i2c_bme.scan()
        print(f"I2Cデバイス検出: {devices}")  # [118] または [119] なら正常
        
        if not devices:
            print("I2Cデバイスが見つかりません")
            return False
            
        # BME280の初期化
        bme = bme280.BME280(i2c=i2c_bme)
        print("BME280センサーが正常に初期化されました")
        return True
        
    except Exception as e:
        print(f"BME280初期化エラー: {e}")
        return False

def connect_wifi():
    """WiFiに接続"""
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    
    if not wlan.isconnected():
        print("WiFiに接続中...")
        wlan.connect(SSID, PASSWORD)
        
        timeout = 10
        while not wlan.isconnected() and timeout > 0:
            time.sleep(1)
            timeout -= 1
            print(".", end="")
        
        if wlan.isconnected():
            print(f"\nWiFi接続成功: {wlan.ifconfig()}")
            return wlan.ifconfig()[0]  # IPアドレスを返す
        else:
            print("WiFi接続に失敗しました")
            return None
    else:
        print(f"既にWiFiに接続済み: {wlan.ifconfig()}")
        return wlan.ifconfig()[0]

def handle_client(client_socket):
    """クライアントからのリクエストを処理"""
    try:
        # データ受信（最大1024バイト）
        data = client_socket.recv(1024)
        if data:
            message = data.decode('utf-8')
            print(f"受信メッセージ: {message}")
            
            # JSONデータの解析
            try:
                request = json.loads(message)
                command = request.get("command")
                
                # コマンドに応じた処理
                if command == "led_on":
                    led.on()
                    response = {"status": "success", "message": "LED点灯", "led_state": "on", "pico_id": PICO_ID}
                elif command == "led_off":
                    led.off()
                    response = {"status": "success", "message": "LED消灯", "led_state": "off", "pico_id": PICO_ID}
                elif command == "get_status":
                    response = {"status": "success", "message": "Pico W is running", "uptime": time.ticks_ms(), "pico_id": PICO_ID}
                elif command == "ping":
                    response = {"status": "success", "message": "pong", "pico_id": PICO_ID}
                elif command == "get_sensor_data":
                    if bme:
                        try:
                            # 参考プログラムと同じ方法でデータを取得
                            temp, pres, hum = bme.read_compensated_data()
                            sensor_data = {
                                "temperature": round(float(temp), 2),
                                "pressure": round(float(pres) / 100, 2),  # Paから hPaに変換
                                "humidity": round(float(hum), 2),
                                "timestamp": time.ticks_ms()
                            }
                            response = {"status": "success", "data": sensor_data, "pico_id": PICO_ID}
                        except Exception as e:
                            response = {"status": "error", "message": f"センサー読み取りエラー: {e}", "pico_id": PICO_ID}
                    else:
                        response = {"status": "error", "message": "BME280が初期化されていません", "pico_id": PICO_ID}
                else:
                    response = {"status": "error", "message": "未知のコマンド", "pico_id": PICO_ID}
                
            except:
                # プレーンテキストメッセージの場合
                if message.strip() == "hello":
                    response = {"status": "success", "message": "Hello from Pico W!", "pico_id": PICO_ID}
                else:
                    response = {"status": "success", "message": f"受信: {message}", "pico_id": PICO_ID}
            
            # レスポンス送信
            response_json = json.dumps(response)
            client_socket.send(response_json.encode('utf-8'))
            
    except Exception as e:
        print(f"エラー: {e}")
        error_response = {"status": "error", "message": str(e)}
        client_socket.send(json.dumps(error_response).encode('utf-8'))
    
    finally:
        client_socket.close()

def start_server():
    """サーバーを開始"""
    # WiFi接続
    ip_address = connect_wifi()
    if not ip_address:
        return
    
    # BME280初期化
    init_bme280()
    
    # ソケット作成
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        # サーバーをバインド
        server_socket.bind((ip_address, SERVER_PORT))
        server_socket.listen(5)
        print(f"サーバー開始: {ip_address}:{SERVER_PORT}")
        print("クライアントからの接続を待機中...")
        
        while True:
            try:
                # クライアント接続を受け付け
                client_socket, client_address = server_socket.accept()
                print(f"クライアント接続: {client_address}")
                
                # クライアントリクエストを処理
                handle_client(client_socket)
                
            except KeyboardInterrupt:
                print("\nサーバーを停止します")
                break
            except Exception as e:
                print(f"接続エラー: {e}")
                continue
    
    finally:
        server_socket.close()

# メイン実行
if __name__ == "__main__":
    start_server()
