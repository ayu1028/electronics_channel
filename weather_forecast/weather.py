import network
import time
import requests

# Wi-Fiの接続情報（書き換えてください）
SSID = "Your WiFi SSID"
PASSWORD = "Your WiFi password"
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
        
    except Exception as e:
        print("エラーが発生しました:", e)

# メイン処理
if __name__ == "__main__":
    if connect_wifi():
        fetch_jma_weather()