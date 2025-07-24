# 指定距離の走行確認

<div class="meta-info">

**Create date:** 2025-07-24  
**Modified date:** 2025-07-24

</div>

**実施日**: 2025/7/24 (Thu) 13:00 -- 14:30  

```admonish todo
**実験の様子を写真に残しておいてください**
```

## 作業分担（2名1組）
**全体（13:00-14:30）：協力作業**
- 協力してプログラミング実験を実施

## 実験内容
### 1. オドメトリ計算
エンコーダーのカウント値からタイヤの移動距離を求めました．
両輪の走行距離情報を用いて，ロボットの現在位置を計算して
表示するプログラムを作成してください．

### 1. 指定距離直進制御
走行速度と走行時間指定で，指定距離を走行してください．

### 2. 180度その場旋回制御
その場旋回をする動作指令を考え，旋回動作をしてください．

### 3. 直角コースの制御
1, 2 を組み合わせ，直角コース往復の制御をしてみてください．

## プログラム例

```python
"""
このプログラムは，ロボット制御基礎の移動ロボット制御プログラムです．
エンコーダー付きDCモーターを，PicoRobotics拡張ボードを用いて，
動作指令を実行します．
また，接続しているOLEDディスプレイへの表示，超音波センサー計測も
合わせて実行する機能があります．
"""

# 最初に，最低限必要なモジュールをインポートし，1秒待機して起動を待つ
from machine import Pin, PWM, reset, time_pulse_us, I2C
import time
time.sleep(1)

# 続いて，詳細機能に必要なモジュールをインポートして，1秒待機して起動を待つ
import PicoRobotics
import utime
#import ssd1306
import math
time.sleep(1)

"""
メイン処理
"""
def main():
    # 最後に画面を更新した時刻を記録
    # 画面更新ごとにlast_printも更新する
    last_print = utime.ticks_ms()
    # 画面更新をする頻度[msec]
    REFRESH_TIME = 100
    
    """
    以下の動作1〜を，必要に応じて削除・追加して，設定コースを走行
    するように記述する．
    """
    ## 動作1: 直進
    START_TIME = utime.ticks_ms()
    while True:
        now = utime.ticks_ms()
        if utime.ticks_diff(now, last_print) > REFRESH_TIME:
            display_shell(count_L, count_R)
            #display.fill(0)  # ディスプレイをクリア
            #display_show(count_L, count_R)
            #display.show()  # ディスプレイに表示

            last_print = now
        
        # 回転方向・速度指令
        board.motorOn(1, "f", 50)
        board.motorOn(2, "f", 50)
        
        if utime.ticks_diff(now, START_TIME) > 3000:
            break

    ## 動作2: 旋回
    START_TIME = utime.ticks_ms()
    while True:
        now = utime.ticks_ms()
        if utime.ticks_diff(now, last_print) > REFRESH_TIME:
            display_shell(count_L, count_R)
            #display.fill(0)  # ディスプレイをクリア
            #display_show(count_L, count_R)
            #display.show()  # ディスプレイに表示

            last_print = now
            
        # 回転方向・速度指令
        board.motorOn(1, "f", 25)
        board.motorOn(2, "r", 25)
        
        if utime.ticks_diff(now, START_TIME) > 650*2:
            break

    ## 動作3: 直進
    START_TIME = utime.ticks_ms()
    while True:
        now = utime.ticks_ms()
        if utime.ticks_diff(now, last_print) > REFRESH_TIME:
            display_shell(count_L, count_R)
            #display.fill(0)  # ディスプレイをクリア
            #display_show(count_L, count_R)
            #display.show()  # ディスプレイに表示

            last_print = now

        # 回転方向・速度指令
        board.motorOn(1, "f", 50)
        board.motorOn(2, "f", 50)
        
        if utime.ticks_diff(now, START_TIME) > 3000:
            break


    # 終了処理．モーターを停止させ，countの最終値を表示して終わる
    # 再度実行する場合は，電源を入れ直す（Thonnyが接続されていれば，再生ボタンを押す）
    board.motorOn(1, "f", 0)
    board.motorOn(2, "f", 0)
    display.fill(0)  # ディスプレイをクリア
    display_shell(count_L, count_R)
    display_show(count_L, count_R)
    display.show()  # ディスプレイに表示


# ロボットの諸定数を定義する
WHEEL_RADIUS = 0.034        # [m]
GEAR_RATIO = 19
ENCODER_PPR = 11            # [pulses/revolution]
DISTANCE_PER_PULSE = (2 * 3.14159 * WHEEL_RADIUS) / (GEAR_RATIO * ENCODER_PPR)


# ディスプレイの設定を行う
# 接続に失敗すると，エラーメッセージを表示して停止する
#i2c = I2C(1, sda=Pin(6), scl=Pin(7))
#try:
#    display = ssd1306.SSD1306_I2C(128, 64, i2c)
#    display.fill(0)  # ディスプレイをクリア
#    display.text("Set up done", 0, 0)
#    display.show()  # ディスプレイに表示
#except:
#    print("Display Error")
#    raise SystemExit

# エンコーダーの設定
# エンコーダピン（AB相）を両輪分定義
pin_a = Pin(16, Pin.IN, Pin.PULL_UP)
pin_b = Pin(15, Pin.IN, Pin.PULL_UP)
pin_c = Pin(10, Pin.IN, Pin.PULL_UP)
pin_d = Pin(11, Pin.IN, Pin.PULL_UP)
# エンコーダ読み取り用グローバル変数
# エンコーダー読み取りは割り込み処理をする．値をバックグラウンドで更新したいので
# グローバル変数として定義している
count_L = 0
last_state_L = 0
count_R = 0
last_state_R = 0

# エンコーダー読み取り関数
# --- 現在の状態をビットで取得（00〜11）
def read_encoder_L_state():
    return (pin_a.value() << 1) | pin_b.value()

def read_encoder_R_state():
    return (pin_c.value() << 1) | pin_d.value()

# --- 割り込み処理（両相変化対応）
def encoder_L_callback(pin):
    global count_L, last_state_L
    new_state = read_encoder_L_state()
    transition = (last_state_L << 2) | new_state
    # 有効な状態遷移パターンで方向を判断（グレイコード順）
    if transition in [0b0001, 0b0111, 0b1110, 0b1000]:  # 正方向
        count_L += 1
    elif transition in [0b0010, 0b0100, 0b1101, 0b1011]:  # 逆方向
        count_L -= 1
    # その他（グリッチ）は無視
    last_state_L = new_state
    
def encoder_R_callback(pin):
    global count_R, last_state_R
    new_state = read_encoder_R_state()
    transition = (last_state_R << 2) | new_state
    # 有効な状態遷移パターンで方向を判断（グレイコード順）
    if transition in [0b0001, 0b0111, 0b1110, 0b1000]:  # 正方向
        count_R += 1
    elif transition in [0b0010, 0b0100, 0b1101, 0b1011]:  # 逆方向
        count_R -= 1
    # その他（グリッチ）は無視
    last_state_R = new_state


# --- 割り込み設定（両エッジ両ピン）
pin_a.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=encoder_L_callback)
pin_b.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=encoder_L_callback)

pin_c.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=encoder_R_callback)
pin_d.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=encoder_R_callback)

# --- 初期状態を保存（pin_a~dが定義された後に実行）
last_state_L = read_encoder_L_state()
last_state_R = read_encoder_R_state()


# ボードとモーター設定
board = PicoRobotics.KitronikPicoRobotics()
board.motorOn(1, "f", 0)
board.motorOn(2, "f", 0)

# 画面表示（シェル）
def display_shell(count_L, count_R):
    print("CountL:", count_L)
    print("CountR:", count_R)
    
# 画面表示（OLED）
def display_show(count_L, count_R):
    dist_L = -count_L * DISTANCE_PER_PULSE
    dist_R =  count_R * DISTANCE_PER_PULSE
    
    #display.text("CountL: {}".format(-count_L), 0,  0)
    #display.text("CountR: {}".format(count_R),  0, 10)
    #display.text("DIST_L: {}".format(dist_L),   0, 20)
    #display.text("DIST_R: {}".format(dist_R),   0, 30)

main()
```

---

## トラブルシューティング

### モーター制御でエラーが発生する場合

#### OSError: [Errno 5] EIO エラー
**症状：** `board.motorOn()`実行時にI/Oエラーが発生

**主な原因と対処法：**
1. **金属部品のショート**
   - エンコーダー基板周辺でネジなどの金属部品が吸着していないか確認
   - 異物を除去し，金属部品が基板に接触していないことを確認

2. **配線の問題**
   - モーター配線が正しく接続されているか確認
   - 配線の断線や接触不良がないか確認

3. **電源の問題**
   - バッテリー残量を確認
   - 電源供給が安定しているか確認

#### 超音波センサーで異常な値が表示される場合
**症状：** 距離測定で`None`や異常に大きな値が返される

**対処法：**
- センサー前方に障害物がないか確認
- TRIGピン，ECHOピンの配線確認
- センサーの向きが正しいか確認

#### プログラムが途中で停止する場合
**対処法：**
- エラーメッセージを確認し，該当するエラーの対処法を実施
- ハードウェアの接続状態を再確認
- プログラムを最初から再実行

