from machine import Pin
import time

# Pin
scan = Pin(15, Pin.IN, Pin.PULL_UP)

wait = 40000

CSV_FILE = "signal_data.csv"

def scanSignal():
    buffer = [0]*1024
    current_time = 0
    current_state = 0
    last_state = 0
    offset = 0
    
    last_state = scan.value()
    
    print("受信開始")
    while True:
        current_time = time.ticks_us()
        if offset and time.ticks_diff(current_time, buffer[offset - 1]) > wait:
            break

        current_state = scan.value()
        if current_state != last_state:
            buffer[offset] = current_time
            offset += 1
            last_state = current_state
            
        if offset >= len(buffer):
            break

    print("受信完了")

    data = []
    for i in range(1, offset):
        data_n = time.ticks_diff(buffer[i], buffer[i-1])
        data.append(data_n)
        
    print(data)
    return data
    
def detect_ir_format(signal):
    print(f"総データ数: {len(signal)}\n")
    
    # 許容誤差（±30%程度を許容）
    def is_match(val, target, tolerance=0.3):
        return target * (1 - tolerance) <= val <= target * (1 + tolerance)

    i = 0
    frame_index = 1
    
    # 配列の中からON/OFFのペアを順番にスキャン
    while i < len(signal) - 1:
        mark = signal[i]     # ONの時間
        space = signal[i+1]  # OFFの時間
        
        format_name = None
        
        # リーダーコードの判定
        # 1. NECフォーマット: Leader ON 9000us, OFF 4500us
        if is_match(mark, 9000) and is_match(space, 4500):
            format_name = "NEC"
        # 2. AEHA(家電協)フォーマット: Leader ON 3400us, OFF 1700us
        elif is_match(mark, 3400) and is_match(space, 1700):
            format_name = "AEHA"
        # 3. SONYフォーマット: Leader ON 2400us, OFF 600us
        elif is_match(mark, 2400) and is_match(space, 600):
            format_name = "SONY"
            
        # フォーマットが特定できた場合のみ出力
        if format_name:
            print(f"▼ フレーム {frame_index} (配列インデックス {i}〜{i+1})")
            print(f"リーダーコード: ON={mark}us, OFF={space}us")
            print(f"推測フォーマット: 【 {format_name} 】\n")
            frame_index += 1
            
        # 次のON/OFFペアへ進む
        i += 2

def init_csv():
    try:
        with open(CSV_FILE, "r") as f:
            pass
    except OSError:
        with open(CSV_FILE, "w") as f:
            f.write("signals\n")
        print("新規CSVファイルを作成しました。")
        
def write_data(data):
    with open(CSV_FILE, "a") as f:
        for i in range(len(data)):
            f.write(f"{data[i]},")
        f.write("\n")

try:
    init_csv()
    while True:
        signal = scanSignal()
        if len(signal) > 5:
            detect_ir_format(signal)
            write_data(signal)
        else:
            print("信号が短すぎます")
        
        time.sleep_ms(100)

except KeyboardInterrupt:
    pass
