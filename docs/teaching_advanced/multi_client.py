import socket
import json
import time
import threading
import csv
import os
from datetime import datetime

class MultiPicoClient:
    def __init__(self, pico_configs):
        """
        複数のPico W用クライアント
        
        Args:
            pico_configs (list): Pico設定のリスト
            例: [{"id": 1, "ip": "192.168.1.100", "port": 8080}, ...]
        """
        self.pico_configs = pico_configs
        self.timeout = 5
        self.monitoring = False
        self.monitor_thread = None
        self.csv_logging = False
        self.csv_filename = None
        self.csv_file = None
        self.csv_writer = None
        
    def send_command_to_pico(self, pico_config, command, data=None):
        """
        指定されたPico Wにコマンドを送信
        
        Args:
            pico_config (dict): Pico設定
            command (str): 送信するコマンド
            data (dict): 追加データ（オプション）
        
        Returns:
            dict: Pico Wからのレスポンス
        """
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.settimeout(self.timeout)
            
            client_socket.connect((pico_config["ip"], pico_config["port"]))
            
            if data:
                message = {"command": command, **data}
            else:
                message = {"command": command}
            
            json_message = json.dumps(message)
            client_socket.send(json_message.encode('utf-8'))
            
            response = client_socket.recv(1024).decode('utf-8')
            
            try:
                response_data = json.loads(response)
                return response_data
            except json.JSONDecodeError:
                return {"status": "error", "message": "Invalid JSON response", "raw_response": response}
        
        except socket.timeout:
            return {"status": "error", "message": "接続タイムアウト", "pico_id": pico_config.get("id")}
        except ConnectionRefusedError:
            return {"status": "error", "message": "接続が拒否されました", "pico_id": pico_config.get("id")}
        except Exception as e:
            return {"status": "error", "message": f"エラー: {str(e)}", "pico_id": pico_config.get("id")}
        finally:
            try:
                client_socket.close()
            except:
                pass
    
    def ping_all(self):
        """全てのPico Wにpingを送信"""
        results = {}
        for pico in self.pico_configs:
            print(f"Pico {pico['id']} ({pico['ip']}) にping送信中...")
            response = self.send_command_to_pico(pico, "ping")
            results[pico['id']] = response
            if response.get("status") == "success":
                print(f"  ✓ Pico {pico['id']}: {response.get('message')}")
            else:
                print(f"  ✗ Pico {pico['id']}: {response.get('message')}")
        return results
    
    def get_all_sensor_data(self):
        """全てのPico Wからセンサーデータを取得"""
        results = {}
        for pico in self.pico_configs:
            response = self.send_command_to_pico(pico, "get_sensor_data")
            results[pico['id']] = response
        return results
    
    def setup_csv_logging(self, filename=None):
        """CSV保存の設定"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"pico_sensor_data_{timestamp}.csv"
        
        self.csv_filename = filename
        
        # CSVヘッダーの作成（台数に応じた列形式）
        headers = ["timestamp", "datetime"]
        for pico in self.pico_configs:
            pico_id = pico["id"]
            headers.extend([
                f"pico{pico_id}_temp",
                f"pico{pico_id}_pressure", 
                f"pico{pico_id}_humidity",
                f"pico{pico_id}_status"
            ])
        
        # CSVファイルを開いてヘッダーを書き込み
        self.csv_file = open(self.csv_filename, 'w', newline='', encoding='utf-8')
        self.csv_writer = csv.writer(self.csv_file)
        self.csv_writer.writerow(headers)
        self.csv_file.flush()
        
        self.csv_logging = True
        print(f"CSV保存を開始しました: {self.csv_filename}")
        
    def stop_csv_logging(self):
        """CSV保存の停止"""
        if self.csv_logging and self.csv_file:
            self.csv_file.close()
            self.csv_logging = False
            print(f"CSV保存を停止しました: {self.csv_filename}")
    
    def save_to_csv(self, results):
        """センサーデータをCSVに保存"""
        if not self.csv_logging or not self.csv_writer:
            return
            
        try:
            # タイムスタンプ
            now = datetime.now()
            timestamp = int(now.timestamp())
            datetime_str = now.strftime("%Y-%m-%d %H:%M:%S")
            
            # データ行の作成
            row = [timestamp, datetime_str]
            
            for pico in self.pico_configs:
                pico_id = pico["id"]
                result = results.get(pico_id, {})
                
                if result.get("status") == "success":
                    data = result.get("data", {})
                    row.extend([
                        data.get("temperature", ""),
                        data.get("pressure", ""),
                        data.get("humidity", ""),
                        "OK"
                    ])
                else:
                    # エラーの場合は空値とエラーステータス
                    row.extend(["", "", "", "ERROR"])
            
            # CSVに書き込み
            self.csv_writer.writerow(row)
            self.csv_file.flush()
            
        except Exception as e:
            print(f"CSV保存エラー: {e}")
    
    def display_sensor_data(self, results):
        """センサーデータを見やすく表示"""
        print(f"[{datetime.now().strftime('%H:%M:%S')}] センサーデータ:")
        for pico_id, response in results.items():
            if response.get("status") == "success":
                data = response.get("data", {})
                print(f"  Pico {pico_id}: 温度={data.get('temperature', 'N/A')}°C, "
                      f"気圧={data.get('pressure', 'N/A')}hPa, "
                      f"湿度={data.get('humidity', 'N/A')}%")
            else:
                print(f"  Pico {pico_id}: エラー - {response.get('message')}")
        
        # CSV保存が有効な場合は保存
        if self.csv_logging:
            self.save_to_csv(results)
    
    def start_monitoring(self, interval=5):
        """全Picoのセンサーデータを定期取得開始"""
        self.monitoring = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop, args=(interval,))
        self.monitor_thread.daemon = True
        self.monitor_thread.start()
        print(f"定期取得を開始しました（間隔: {interval}秒）")
    
    def stop_monitoring(self):
        """定期取得を停止"""
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join()
        print("定期取得を停止しました")
        
        # CSV保存も停止
        if self.csv_logging:
            self.stop_csv_logging()
    
    def _monitor_loop(self, interval):
        """定期取得のメインループ"""
        while self.monitoring:
            try:
                results = self.get_all_sensor_data()
                self.display_sensor_data(results)
                time.sleep(interval)
            except Exception as e:
                print(f"監視エラー: {e}")
                time.sleep(1)
    
    def control_led(self, pico_id, action):
        """指定されたPicoのLEDを制御"""
        pico_config = next((p for p in self.pico_configs if p['id'] == pico_id), None)
        if not pico_config:
            return {"status": "error", "message": f"Pico {pico_id} が見つかりません"}
        
        command = "led_on" if action == "on" else "led_off"
        return self.send_command_to_pico(pico_config, command)
    
    def get_status_all(self):
        """全てのPico Wのステータスを取得"""
        results = {}
        for pico in self.pico_configs:
            response = self.send_command_to_pico(pico, "get_status")
            results[pico['id']] = response
        return results

def main():
    """メイン関数"""
    print("複数Pico W センサー監視システム")
    print("=" * 40)
    
    # Pico設定を入力
    pico_configs = []
    #num_picos = int(input("Picoの台数を入力してください (1-3): "))
    #
    #for i in range(num_picos):
    #    print(f"\nPico {i+1} の設定:")
    #    ip = input(f"  IPアドレス: ").strip()
    #    port = int(input(f"  ポート番号 (デフォルト: 8080): ") or 8080)
    #    pico_configs.append({"id": i+1, "ip": ip, "port": port})
    pico_configs.append({"id": 1, "ip": "192.168.11.5", "port":8080})
    #pico_configs.append({"id": 2, "ip": "192.168.11.XX", "port":8080})
    #pico_configs.append({"id": 3, "ip": "192.168.11.XX", "port":8080})
    
    # クライアント作成
    client = MultiPicoClient(pico_configs)
    
    print("\n接続テスト中...")
    client.ping_all()
    
    print("\nコマンド一覧:")
    print("  ping      - 全Picoにpingを送信")
    print("  sensor    - 全Picoからセンサーデータを取得")
    print("  monitor   - センサーデータの定期取得を開始/停止")
    print("  csv       - CSV保存の開始/停止")
    print("  led       - 指定PicoのLED制御")
    print("  status    - 全Picoのステータスを取得")
    print("  quit      - 終了")
    print()
    
    monitoring = False
    
    while True:
        try:
            if not monitoring:
                command = input("コマンドを入力してください: ").strip().lower()
            else:
                command = input("コマンドを入力してください (monitor中): ").strip().lower()
            
            if command == "quit":
                if monitoring:
                    client.stop_monitoring()
                print("終了します")
                break
            
            elif command == "ping":
                client.ping_all()
            
            elif command == "sensor":
                results = client.get_all_sensor_data()
                client.display_sensor_data(results)
            
            elif command == "monitor":
                if not monitoring:
                    interval = int(input("取得間隔（秒）を入力してください (デフォルト: 5): ") or 5)
                    client.start_monitoring(interval)
                    monitoring = True
                else:
                    client.stop_monitoring()
                    monitoring = False
            
            elif command == "csv":
                if not client.csv_logging:
                    filename = input("CSVファイル名を入力してください (空白で自動生成): ").strip()
                    if not filename:
                        filename = None
                    client.setup_csv_logging(filename)
                else:
                    client.stop_csv_logging()
            
            elif command == "led":
                pico_id = int(input("制御するPico ID (1-3): "))
                action = input("動作 (on/off): ").strip().lower()
                response = client.control_led(pico_id, action)
                print(f"LED制御結果: {response}")
            
            elif command == "status":
                results = client.get_status_all()
                print("ステータス一覧:")
                for pico_id, response in results.items():
                    if response.get("status") == "success":
                        uptime = response.get("uptime", "N/A")
                        print(f"  Pico {pico_id}: 稼働中 (uptime: {uptime}ms)")
                    else:
                        print(f"  Pico {pico_id}: エラー - {response.get('message')}")
            
            else:
                print("無効なコマンドです")
            
            print()
            
        except KeyboardInterrupt:
            print("\n終了します")
            if monitoring:
                client.stop_monitoring()
                monitoring = False
        except Exception as e:
            print(f"エラー: {e}")

if __name__ == "__main__":
    main()
