import pandas as pd
import emoji
from collections import Counter

def process_regular_csv(filename):
   print(f"\n{filename}の読み込み開始")
   
   # CSVファイルを直接読み込んで内容を確認
   with open(filename, 'r', encoding='utf-8') as f:
       # 最初の行（統計情報）をスキップ
       next(f)
       # データを行ごとに読み込む
       rows = []
       for line in f:
           # 最初のカンマまでをテキストとして取得
           text = line.split(',')[0]
           rows.append(text)
   
   print(f"\n読み込まれた行数: {len(rows)}")
   print("\n最初の5行のテキスト内容:")
   for i, text in enumerate(rows[:5]):
       print(f"行 {i}: {text}")
   
   return rows

def process_special_csv(filename):
   print(f"\n{filename}の読み込み開始")
   
   # 特別な形式のCSVファイルを読み込む
   with open(filename, 'r', encoding='utf-8') as f:
       rows = []
       for line in f:
           # 最初のカンマまでをテキストとして取得
           text = line.split(',')[0]
           rows.append(text)
   
   print(f"\n読み込まれた行数: {len(rows)}")
   print("\n最初の5行のテキスト内容:")
   for i, text in enumerate(rows[:5]):
       print(f"行 {i}: {text}")
   
   return rows

def extract_emojis(text):
   emojis = [char for char in str(text) if emoji.is_emoji(char)]
   return emojis

def analyze_emoji_usage(texts):
   single_emoji = 0
   multiple_emoji = 0
   total_texts_with_emoji = 0
   
   print("\n絵文字の検出処理開始")
   emoji_examples = {'single': [], 'multiple': []}  # 例を保存するための辞書
   
   for text in texts:
       emojis = extract_emojis(text)
       if len(emojis) > 0:
           total_texts_with_emoji += 1
           if len(emojis) == 1:
               single_emoji += 1
               if len(emoji_examples['single']) < 3:  # 単一絵文字の例を3つまで保存
                   emoji_examples['single'].append(text)
           else:
               multiple_emoji += 1
               if len(emoji_examples['multiple']) < 3:  # 複数絵文字の例を3つまで保存
                   emoji_examples['multiple'].append(text)
   
   return {
       'total_texts': len(texts),
       'texts_with_emoji': total_texts_with_emoji,
       'single_emoji': single_emoji,
       'multiple_emoji': multiple_emoji,
       'examples': emoji_examples
   }

# 全ファイルのリスト
csv_files = ['jp_1.csv', 'jp_2.csv', 'jp_3.csv', 'jp_4.csv']

# 全体の統計を保持する辞書
total_stats = {
   'total_texts': 0,
   'texts_with_emoji': 0,
   'single_emoji': 0,
   'multiple_emoji': 0,
   'examples': {'single': [], 'multiple': []}
}

# 各ファイルの処理
for file in csv_files:
   try:
       print(f"\n=== {file} の処理 ===")
       
       if file == 'jp_3.csv':
           texts = process_special_csv(file)
       else:
           texts = process_regular_csv(file)
       
       stats = analyze_emoji_usage(texts)
       
       # 各ファイルの結果を表示
       print(f"\n{file} の分析結果:")
       print(f"総テキスト数: {stats['total_texts']}")
       print(f"絵文字を含むテキスト数: {stats['texts_with_emoji']}")
       if stats['texts_with_emoji'] > 0:
           print(f"絵文字1個使用: {stats['single_emoji']} ({(stats['single_emoji']/stats['texts_with_emoji']*100):.1f}%)")
           print(f"絵文字複数使用: {stats['multiple_emoji']} ({(stats['multiple_emoji']/stats['texts_with_emoji']*100):.1f}%)")
       
       # 全体の統計に加算
       total_stats['total_texts'] += stats['total_texts']
       total_stats['texts_with_emoji'] += stats['texts_with_emoji']
       total_stats['single_emoji'] += stats['single_emoji']
       total_stats['multiple_emoji'] += stats['multiple_emoji']
       
       # 例を追加（最大3つまで）
       for category in ['single', 'multiple']:
           for example in stats['examples'][category]:
               if len(total_stats['examples'][category]) < 3:
                   total_stats['examples'][category].append(f"[{file}] {example}")

   except FileNotFoundError:
       print(f"警告: {file}が見つかりませんでした")
   except Exception as e:
       print(f"エラー: {file}の処理中にエラーが発生しました - {str(e)}")

# 全体の結果を表示
print("\n=== 全ファイルの合計結果 ===")
print(f"総テキスト数: {total_stats['total_texts']}")
print(f"絵文字を含むテキスト数: {total_stats['texts_with_emoji']}")
if total_stats['texts_with_emoji'] > 0:
   print(f"絵文字1個使用: {total_stats['single_emoji']} ({(total_stats['single_emoji']/total_stats['texts_with_emoji']*100):.1f}%)")
   print(f"絵文字複数使用: {total_stats['multiple_emoji']} ({(total_stats['multiple_emoji']/total_stats['texts_with_emoji']*100):.1f}%)")
   
   print("\n=== 例 ===")
   print("単一絵文字の例:")
   for example in total_stats['examples']['single']:
       print(f"- {example}")
   print("\n複数絵文字の例:")
   for example in total_stats['examples']['multiple']:
       print(f"- {example}")