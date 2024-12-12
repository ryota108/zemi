import pandas as pd
import emoji

# CSVファイルを読み込む
df = pd.read_csv('emoji_rows_only.csv', header=None, names=['text'])

# 絵文字の個数をカウントする関数
def count_emojis(text):
    return sum(emoji.is_emoji(char) for char in str(text))

# 各行のテキストと絵文字の個数を抽出してリストに格納
rows_list = []
for text in df['text']:
    emoji_count = count_emojis(text)
    rows_list.append({'text': text, 'emoji_count': emoji_count})

# リストをDataFrameに変換してCSVファイルに出力
rows_df = pd.DataFrame(rows_list)
rows_df.to_csv('emoji_counts.csv', index=False)

# 結果を表示する
print(f"{len(rows_df)} 行のテキストと絵文字の個数を 'emoji_counts.csv' に出力しました。")
for _, row in rows_df.iterrows():
    print(f"テキスト: '{row['text']}', 絵文字の個数: {row['emoji_count']}")