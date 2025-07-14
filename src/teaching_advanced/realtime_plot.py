# PC側プログラム：Picoからのデータをリアルタイムでグラフ表示
import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque
import re
import datetime

# シリアル通信設定（適切なCOMポートに変更してください）
# Windows: 'COM3', 'COM4' など
# macOS/Linux: '/dev/ttyACM0', '/dev/cu.usbmodem*' など
SERIAL_PORT = '/dev/cu.usbmodem*'  # macOS例（実際のポート名に変更）
BAUD_RATE = 115200

# データ保存用（最大100データポイント）
max_len = 100
time_data = deque(maxlen=max_len)
temp_data = deque(maxlen=max_len)
pres_data = deque(maxlen=max_len)
humi_data = deque(maxlen=max_len)

# グラフ設定
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 8))
fig.suptitle('BME280 センサー データ（リアルタイム）', fontsize=14)

# 初期化
line1, = ax1.plot([], [], 'r-', label='温度 (°C)')
line2, = ax2.plot([], [], 'g-', label='気圧 (hPa)')
line3, = ax3.plot([], [], 'b-', label='湿度 (%)')

# 軸設定
ax1.set_ylabel('温度 (°C)')
ax1.grid(True)
ax1.legend()

ax2.set_ylabel('気圧 (hPa)')
ax2.grid(True)
ax2.legend()

ax3.set_ylabel('湿度 (%)')
ax3.set_xlabel('時間')
ax3.grid(True)
ax3.legend()

# シリアル接続
try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    print(f"シリアルポート {SERIAL_PORT} に接続しました")
except Exception as e:
    print(f"シリアル接続エラー: {e}")
    print("ポート名を確認して SERIAL_PORT を適切に設定してください")
    exit()

def parse_sensor_data(line):
    """
    Picoからの出力をパース
    想定フォーマット: "気温: 25.30°C  気圧: 1013.25hPa  湿度: 45.60%"
    """
    try:
        # 正規表現でデータを抽出
        temp_match = re.search(r'気温:\s*([\d.]+)', line)
        pres_match = re.search(r'気圧:\s*([\d.]+)', line)
        humi_match = re.search(r'湿度:\s*([\d.]+)', line)
        
        if temp_match and pres_match and humi_match:
            temp = float(temp_match.group(1))
            pres = float(pres_match.group(1))
            humi = float(humi_match.group(1))
            return temp, pres, humi
        return None
    except Exception as e:
        print(f"データパース エラー: {e}")
        return None

def update_plot(frame):
    """アニメーション更新関数"""
    try:
        # シリアルデータ読み取り
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8', errors='ignore').strip()
            
            if line:
                # データをパース
                result = parse_sensor_data(line)
                if result:
                    temp, pres, humi = result
                    current_time = datetime.datetime.now()
                    
                    # データを追加
                    time_data.append(current_time)
                    temp_data.append(temp)
                    pres_data.append(pres)
                    humi_data.append(humi)
                    
                    # グラフ更新
                    if len(time_data) > 1:
                        line1.set_data(range(len(temp_data)), temp_data)
                        line2.set_data(range(len(pres_data)), pres_data)
                        line3.set_data(range(len(humi_data)), humi_data)
                        
                        # 軸の範囲を自動調整
                        for ax, data in [(ax1, temp_data), (ax2, pres_data), (ax3, humi_data)]:
                            if data:
                                ax.set_xlim(0, len(data)-1)
                                ax.set_ylim(min(data) - 1, max(data) + 1)
                        
                        # X軸のラベルを時間に（最後の5つのみ表示）
                        if len(time_data) >= 5:
                            tick_positions = list(range(len(time_data)-5, len(time_data)))
                            tick_labels = [t.strftime('%H:%M:%S') for t in list(time_data)[-5:]]
                            ax3.set_xticks(tick_positions)
                            ax3.set_xticklabels(tick_labels, rotation=45)
                    
                    print(f"受信: 温度={temp:.1f}°C, 気圧={pres:.1f}hPa, 湿度={humi:.1f}%")
                
    except Exception as e:
        print(f"更新エラー: {e}")
    
    return line1, line2, line3

# データ保存機能
def save_data():
    """データをCSVファイルに保存"""
    if time_data and temp_data:
        filename = f"sensor_data_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        with open(filename, 'w') as f:
            f.write("時刻,温度(°C),気圧(hPa),湿度(%)\n")
            for i in range(len(time_data)):
                f.write(f"{time_data[i]},{temp_data[i]},{pres_data[i]},{humi_data[i]}\n")
        print(f"データを {filename} に保存しました")

# アニメーション開始
print("データ受信を開始します...")
print("グラフウィンドウを閉じると終了します")

try:
    ani = animation.FuncAnimation(fig, update_plot, interval=1000, blit=False)
    plt.tight_layout()
    plt.show()
except KeyboardInterrupt:
    print("プログラムを停止します")
finally:
    # 終了時にデータを保存
    save_data()
    ser.close()
    print("シリアル接続を閉じました")