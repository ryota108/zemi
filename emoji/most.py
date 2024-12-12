import pandas as pd
import emoji
from collections import Counter

def process_regular_csv(filename):
    # 最初の行をスキップし、データ型を指定して読み込む
    df = pd.read_csv(filename, 
                     skiprows=1,  # 最初の行をスキップ
                     quotechar='"', 
                     escapechar='\\', 
                     header=None,
                     names=['text', 'col2', 'date', 'lang', 'col5', 'col6'])
    
    print(f"\n{filename}の最初の数行:")
    print(df.head())
    return df['text']

def process_special_csv(filename):
    df = pd.read_csv(filename, quotechar='"', escapechar='\\', header=None, 
                     names=['text', 'col2', 'col3'])
    return df['text']

def extract_emojis(text):
    emojis = [char for char in str(text) if emoji.is_emoji(char)]
    if emojis:  # デバッグ用出力
        print(f"テキスト: {text}")
        print(f"検出された絵文字: {emojis}")
    return emojis

# 処理するCSVファイルのリスト
csv_files = ['jp_1.csv', 'jp_2.csv', 'jp_3.csv', 'jp_4.csv']

# すべてのCSVファイルから絵文字を抽出
all_emojis = []
for file in csv_files:
    try:
        print(f"\n処理中のファイル: {file}")
        
        # en_3.csvの場合は特別な処理を行う
        if file == 'jp_3.csv':
            texts = process_special_csv(file)
        else:
            texts = process_regular_csv(file)
        
        emoji_list = []
        for text in texts:
            emojis = extract_emojis(text)
            emoji_list.extend(emojis)
        
        all_emojis.extend(emoji_list)
        print(f"{file}から抽出された絵文字数:", len(emoji_list))
        
    except FileNotFoundError:
        print(f"警告: {file}が見つかりませんでした")
    except Exception as e:
        print(f"エラー: {file}の処理中にエラーが発生しました - {str(e)}")

print("\n全ファイルの絵文字の総数:", len(all_emojis))

# 絵文字の出現回数をカウント
emoji_counts = Counter(all_emojis)

# 上位5個の絵文字とその使用回数を取得
print("\n上位5個の絵文字とその使用回数:")
top_5_emojis = emoji_counts.most_common(5)
for emoji, count in top_5_emojis:
    print(f"絵文字: {emoji}, 使用回数: {count}")