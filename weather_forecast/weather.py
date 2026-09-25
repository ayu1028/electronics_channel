import network
import time
import requests
from machine import Pin, I2C
import json

with open("config.json", "r") as f:
    config = json.load(f)

i2c = I2C(0, scl=Pin(17), sda=Pin(16), freq=100000)
ATP3012_ADDR = 0x2E
buf = bytearray(1)
buf[0] = 0xFF

word_list = {
  "から": "ka'ra",
  "くもり": "kumori",
  "で": "de",
  "まで": "ma'de",
  "を伴う": "o tomonau",
  "一時": "ichi'ji",
  "夕方": "yu-gata",
  "夜": "yoru",
  "夜のはじめ頃": "yoru no hajimegoro",
  "夜遅く": "yo'ru/o'soku",
  "所により": "tokoroniyori",
  "明け方": "akegata",
  "昼前": "hirumae",
  "昼過ぎ": "hirusugi",
  "時々": "tokidoki",
  "晴れ": "hare",
  "朝": "asa",
  "朝晩": "asaban",
  "未明": "mimei",
  "激しく": "hageshiku",
  "降る": "furu",
  "雨": "a'me",
  "雷": "kaminari",
  "雷を伴い": "kaminari o tomonai",
  "雷を伴う": "kaminari o tomonau",
  "霧": "kiri"
}

# Wi-Fiの接続情報（書き換えてください）
SSID = config["SSID"]
PASSWORD = config["PASSWORD"]
URL = "https://www.jma.go.jp/bosai/forecast/data/forecast/230000.json"

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    
    if not wlan.isconnected():
        print("Wi-Fiに接続中...")
        wlan.connect(SSID, PASSWORD)
        
        timeout = 10
        while not wlan.isconnected() and timeout > 0:
            time.sleep(1)
            timeout -= 1
            
    if wlan.isconnected():
        print("Wi-Fi接続成功!")
        print("IPアドレス:", wlan.ifconfig()[0])
        return True
    else:
        print("Wi-Fi接続失敗")
        return False

def fetch_jma_weather():
    print(f"\n気象庁APIからデータ取得中: {URL}")
    try:
        response = requests.get(URL)
        
        if response.status_code == 200:
            print("取得成功！データを解析します...\n")
            
            # JSON形式としてパース（Pythonの辞書・リストに変換）
            data = response.json()
            
            # 1. 地域の確定（西部: 名古屋等 / 東部: 豊橋等）
            time_series = data[0]["timeSeries"]
            area_weather = time_series[0]["areas"][0] # 西部エリア
            area_name = area_weather["area"]["name"]
            
            # 2. 今日の天気テロップの取得
            today_weather = area_weather["weathers"][0]
            
            # 3. 降水確率の取得（時間帯ごとに複数格納されているため最後の値を出力例に）
            area_pops = time_series[1]["areas"][0]
            pop_list = area_pops["pops"]
            latest_pop = pop_list[0] if pop_list else "--"
            
            # 4. 気温データの取得（2番目の要素に地点別の予想気温が入っています）
            temps_data = data[0].get("timeSeries", [])[2]["areas"][0]
            temps = temps_data.get("temps", ["--", "--"])
            min_temp = temps[0] if len(temps) > 0 else "--"
            max_temp = temps[1] if len(temps) > 1 else "--"
            
            # 解析結果の出力
            print("=" * 35)
            print(f"【{area_name}の天気予報】")
            print(f"天気      : {today_weather}")
            print(f"直近降水確率: {latest_pop}%")
            print(f"予想気温  : 最低 {min_temp}℃ / 最高 {max_temp}℃")
            print("=" * 35)
            
        else:
            print(f"取得失敗。ステータスコード: {response.status_code}")
            
        # メモリ解放
        response.close()
        
        return today_weather
        
    except Exception as e:
        print("エラーが発生しました:", e)
        
def talk_with_ATP3012(word):
    i2c.readfrom_into(ATP3012_ADDR, buf)
    time.sleep_ms(20)
    while buf[0] == 0xFF or buf[0] == 0x2A:
        i2c.readfrom_into(ATP3012_ADDR, buf)
        time.sleep_ms(20)
        
    data_to_send = word.encode('utf-8') + b'\r'
    i2c.writeto(ATP3012_ADDR, data_to_send)

# メイン処理
if __name__ == "__main__":
    if connect_wifi():
        weather_words = fetch_jma_weather()
        words = weather_words.replace("　", " ").split()
        print(len(words))
        talk_with_ATP3012("kyo'-no+te'nkiwa")
        for i in range(len(words)):
            word = word_list[words[i]]
            print(word)
            talk_with_ATP3012(word)
#         talk_with_ATP3012("koredei'i?")
            
        