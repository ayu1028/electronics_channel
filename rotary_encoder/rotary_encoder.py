import machine
import utime

# ピンの設定（GP11=A相, GP15=B相）
pin_a = machine.Pin(11, machine.Pin.IN, machine.Pin.PULL_UP)
pin_b = machine.Pin(15, machine.Pin.IN, machine.Pin.PULL_UP)

# 動作確認用のLED (Pico標準のLEDピン、Pico Wの場合は 'LED' 指定になります)
led = machine.Pin(25, machine.Pin.OUT)

print("プログラム開始: Ctrl+C で停止します...")
led.on()

count = 0
last_count = 0

# 前回のA相の状態を記憶する変数 (初期値は現在のPin状態)
last_a_state = pin_a.value()

# チャタリング防止用の時間管理
last_time = utime.ticks_ms()
DEBOUNCE_MS = 5  # デバウンス時間 (5ms)

try:
    while True:
        current_a_state = pin_a.value()
        
        # A相の状態が「HIGH(1) から LOW(0)」へ変化した瞬間（立ち下がり）を検出
        if last_a_state == 1 and current_a_state == 0:
            current_time = utime.ticks_ms()
            
            # デバウンス時間が経過している場合のみカウント処理
            if utime.ticks_diff(current_time, last_time) > DEBOUNCE_MS:
                # A相がLOWに落ちた瞬間のB相の状態をチェック
                if pin_b.value() == 1:
                    count += 1   # 時計回り(CW)
                else:
                    count -= 1   # 反時計回り(CCW)
                
                last_time = current_time
        
        # A相の状態を更新
        last_a_state = current_a_state
        
        # 値が変化したときだけ表示（シリアル表示の負荷を軽減）
        if count != last_count:
            print(f"Count: {count}")
            last_count = count
            
        # CPU負荷軽減用の短いスリープ (1ms)
        utime.sleep_ms(1)

except KeyboardInterrupt:
    print("\nプログラムを停止しました。")
    led.off()