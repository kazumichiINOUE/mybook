# Pico側プログラム：センサーデータをOLEDとシリアル出力
from machine import I2C, Pin
import ssd1306
import time
import bme280_float as bme280

# BME280センサー設定
i2c_bme = I2C(0, scl=Pin(17), sda=Pin(16), freq=100000)
print(i2c_bme.scan())  # [118] または [119] なら正常
bme = bme280.BME280(i2c=i2c_bme)

# LED設定
led = Pin(22, Pin.OUT)
led.value(1)

# OLEDディスプレイ設定
i2c_oled = I2C(1, sda=Pin(6), scl=Pin(7))
try:
    display = ssd1306.SSD1306_I2C(128, 64, i2c_oled)
    print("OLED 初期化完了")
except:
    print("Display Error")
    display = None
    
if display:
    display.fill(0)
    display.text("Set up sensor", 0, 0)
    display.show()

print("センサー計測開始...")

# 計測開始
while True:
    try:
        # センサーデータ読み取り
        temp, pres, humi = bme.read_compensated_data()
        
        # シリアル出力（PC側パース用の統一フォーマット）
        print(f'気温: {temp:.2f}°C  気圧: {pres/100:.2f}hPa  湿度: {humi:.2f}%')
        
        # LED制御（気温25度で切り替え）
        if temp > 25.0:
            led.value(0)  # 点灯
        else:
            led.value(1)  # 消灯
        
        # OLED表示
        if display:
            display.fill(0)
            display.text("Temp.: {:.1f} deg".format(float(temp)), 0,  0)
            display.text("Pres.: {:.0f} hPa".format(float(pres)/100), 0, 10)
            display.text("Humi.: {:.0f} %".format(float(humi)), 0, 20)
            display.show()
        
        time.sleep(1)
        
    except Exception as e:
        print(f"エラー: {e}")
        time.sleep(1)