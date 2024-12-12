import pandas as pd

# CSVファイルを読み込む
df = pd.read_csv('all.csv', header=None)

# 2列目の数値が多い順に1000件取得
top_1000 = df.nlargest(1000, 1)

# 取得したデータを並べ替えてCSVファイルに出力
top_1000.sort_values(by=1, ascending=False).to_csv('top_1000_data.csv', header=False, index=False)

# 結果を表示する
print(f"2列目の数値が多い順に1000件を 'top_1000_data.csv' に出力しました。")
print(top_1000.head())