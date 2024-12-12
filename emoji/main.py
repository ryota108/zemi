import pandas as pd
import emoji

# CSVファイルを読み込む
df = pd.read_csv('emoji_rows_only.csv')

# すべての列をテキスト列として扱う
text_columns = df.columns

# 絵文字の個数をカウントする関数
def count_emojis(text):
    return sum(emoji.is_emoji(char) for char in str(text))

# 各列の2行目のテキストと絵文字の個数を抽出してリストに格納
rows_list = []
for column in text_columns:
    try:
        text = df[column].iloc[0]  # 2行目のテキストを取得
        emoji_count = count_emojis(text)
        rows_list.append({'column': column, 'text': text, 'emoji_count': emoji_count})
    except IndexError:
        print(f"列 '{column}' には2行目がありません。")

# リストをDataFrameに変換してCSVファイルに出力
rows_df = pd.DataFrame(rows_list)
rows_df.to_csv('rows.csv', index=False)

# 結果を表示する
print(f"{len(rows_df)} 行の2行目のテキストと絵文字の個数を 'rows.csv' に出力しました。")
for _, row in rows_df.iterrows():
    print(f"列 '{row['column']}' の2行目: '{row['text']}', 絵文字の個数: {row['emoji_count']}")