import pandas as pd

# CSVファイルを読み込む
df = pd.read_csv('../jp_1.csv', header=None, names=['text', 'id', 'timestamp', 'lang', 'length'])

# !と?の個数をカウントする関数
def count_symbols(text):
    exclamation_count = str(text).count('!')
    question_count = str(text).count('?')
    return exclamation_count, question_count

# 各テキストの!と?の個数をカウント
results = []
for index, row in df.iterrows():
    text = row['text']
    exclamation_count, question_count = count_symbols(text)
    results.append({
        'text': text,
        'exclamation_marks': exclamation_count,
        'question_marks': question_count
    })

# 結果をDataFrameに変換
results_df = pd.DataFrame(results)

# 結果を表示
print("解析結果:")
for index, row in results_df.iterrows():
    print(f"\nテキスト: {row['text']}")
    print(f"!の数: {row['exclamation_marks']}")
    print(f"?の数: {row['question_marks']}")

# 結果をCSVファイルに保存
results_df.to_csv('symbol_counts.csv', index=False)
print("\n結果を'symbol_counts.csv'に保存しました。")