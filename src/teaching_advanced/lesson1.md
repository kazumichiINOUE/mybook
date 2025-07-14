# 講義ノート1回目

<div class="meta-info">

**Create date:** 2025-07-11  
**Modified date:** 2025-07-11

</div>

```admonish info
2025/7/15 (Tue) 16:20 -- 17:50  
**実験の様子を写真に残しておいてください**
```

## 大きな目標設定
- IoTの基礎をマイコンプログラミングを通して学ぶ
- Pythonの文法を知る
<!--
- インターネット通信の仕組みを知る
-->

## 実験内容
1. ブレッドボードで温度センサー計測回路を組み立てる
2. 温度センサーをRaspberryPi Pico で読み取る
3. センサー値をOLEDディスプレイで表示する
4. 計測データをファイルに保存してPCでグラフにする

## 1. ブレッドボードで温度センサー計測回路を組み立てる
### 配線図
![温度センサー配線図](../images/teaching-pico-bme280-wiring.png)

### 完成図
![温度センサー配線完成](../images/teaching-wiring-complete.png)

## 2. 温度センサーをRaspberryPi Pico で読み取る
### センサー利用のためのPythonモジュールをセット
1. 以下のURLにブラウザでアクセスする  
[GitHub - robert-hh/BME280: Micropython driver for the BME280 sensor](https://github.com/robert-hh/BME280/tree/master)
    
2. 今回使うモジュール名をクリックする  
![bme280の場所.png](../images/teaching-bme280-location.png)
    
3. モジュールのソースコードをコピーボタンでコピーする  
![bme280_floatのコピー.png](../images/teaching-bme280-float-copy.png)
    
4. Thonnyで新しいファイルを作成し，先ほどコピーしたソースコードをペーストする  
![bme280を貼り付け.png](../images/teaching-bme280-paste.png)
    
5. ThonnyからPicoを認識させる
6. Picoに `bme280_float.py` という名前で保存する  
![名前をつけて保存.png](../images/teaching-thonny-save-as.png)  
![picoを選択.png](../images/teaching-thonny-select-pico.png)  
![ファイル名を指定して保存.png](../images/teaching-thonny-save-filename.png)  

### センサーからデータ読み取り

1. 以下のプログラムをThonny上に書き，Picoで実行する
```python
from machine import I2C, Pin
import bme280_float as bme280
import time

i2c = I2C(0, scl=Pin(17), sda=Pin(16), freq=100000)
print(i2c.scan())  # [118] または [119] なら正常

bme = bme280.BME280(i2c=i2c)

led = Pin(22, Pin.OUT) # LEDについてはなくても問題ない
led.value(1)           # 

while True:
    # 気温，気圧，湿度を読み取る
    temp, pres, hum = bme.read_compensated_data()
    print('気温: {:.2f}°C  気圧: {:.2f}hPa  湿度: {:.2f}%'.format(temp, pres / 100, hum))

    # (オプション）気温が25度を超えたらLEDを点灯させる
    if temp > 25.0:
        led.value(0)
    else:
        led.value(1)

    # 1秒間隔で計測を続ける
    time.sleep(1)
```
    
2. シェルに以下のような表示が出たら成功．LEDを繋いでいる場合，気温25度を超えると点灯する（点灯を判断する数値は適当を変えてよい）
  <video controls poster="../images/teaching-temperature-sensor-preview.png"
  style="width: 100%; height: auto;">
    <source src="../images/teaching-temperature-sensor-reading.mov"
  </video>

## 3. センサー値をOLEDディスプレイで表示する
### 配線図
![OLED配線図](../images/teaching-pico配線_BME280.png)
### 完成図
![OLED配線図](../images/teaching-pico配線_BME280_完成.jpeg)
### OLED表示付きプログラム
```python
{{#include oled.py}}
```

## 4. 計測データをファイルに保存してPCでグラフにする
[Pythonでグラフが表示されない場合の対処法](matplotlib-troubleshooting.md)
