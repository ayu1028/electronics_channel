import requests
import time

def extract_weather_words():
    # 1. 全国の予報区（office）コード一覧を取得する
    area_url = "https://www.jma.go.jp/bosai/common/const/area.json"
    print(f"エリア情報を取得中: {area_url}")
    
    response = requests.get(area_url)
    response.raise_for_status()
    area_data = response.json()
    
    # officesキーの中に "230000": {"name": "愛知県", ...} のような形で格納されている
    office_codes = list(area_data["offices"].keys())
    print(f"対象エリア数: {len(office_codes)}箇所")
    
    # 重複を排除するためにsetを使用
    unique_words = set()
    
    # 2. 各予報区の天気予報JSONを取得してテロップを解析
    for i, code in enumerate(office_codes):
        forecast_url = f"https://www.jma.go.jp/bosai/forecast/data/forecast/{code}.json"
        
        try:
            res = requests.get(forecast_url)
            if res.status_code == 200:
                forecast_data = res.json()
                
                # data[0]["timeSeries"][0]["areas"] へのアクセス
                time_series = forecast_data[0]["timeSeries"][0]
                for area in time_series.get("areas", []):
                    weathers = area.get("weathers", [])
                    
                    for weather_text in weathers:
                        # 気象庁のデータは全角スペース「 」で区切られていることが多いため
                        # 半角スペースに置換してからsplit()で分割する
                        words = weather_text.replace(" ", " ").split()
                        
                        # 抽出したワードをsetに追加
                        unique_words.update(words)
            
        except Exception as e:
            print(f"取得エラー ({code}): {e}")
            
        # サーバーへの負荷軽減（Dos攻撃にならないよう必ず入れる）
        time.sleep(0.2)
        
        if (i + 1) % 10 == 0:
            print(f"{i + 1}/{len(office_codes)} 箇所の処理が完了...")
            
    # 3. setをリストに変換し、五十音（文字コード）順にソート
    word_list = sorted(list(unique_words))
    return word_list

if __name__ == "__main__":
    print("データ抽出を開始します。数十秒かかります...\n")
    words = extract_weather_words()
    
    print("\n" + "="*30)
    print("抽出された天気ワード一覧")
    print("="*30)
    
    for word in words:
        print(word)
        
    print("="*30)
    print(f"合計: {len(words)} 種類のワードが見つかりました。")
    
    # 必要に応じてファイルに保存（例：JSONやテキスト）
    import json
    with open("weather_words.json", "w", encoding="utf-8") as f:
        json.dump(words, f, ensure_ascii=False, indent=2)