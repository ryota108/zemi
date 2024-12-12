import pandas as pd
import emoji
from collections import Counter

def process_regular_csv(filename):
   print(f"\n{filename}の読み込み開始")
   
   with open(filename, 'r', encoding='utf-8') as f:
       next(f)
       rows = []
       for line in f:
           text = line.split(',')[0]
           rows.append(text)
   
   print(f"読み込まれた行数: {len(rows)}")
   return rows

def process_special_csv(filename):
   print(f"\n{filename}の読み込み開始")
   
   with open(filename, 'r', encoding='utf-8') as f:
       rows = []
       for line in f:
           text = line.split(',')[0]
           rows.append(text)
   
   print(f"読み込まれた行数: {len(rows)}")
   return rows

def extract_emojis(text):
   return [char for char in str(text) if emoji.is_emoji(char)]

def analyze_detailed_emoji_usage(texts):
   emoji_counts = {1: 0, 2: 0, 3: 0, 4: 0, '5+': 0}
   total_texts_with_emoji = 0
   examples = {1: [], 2: [], 3: [], 4: [], '5+': []}
   
   print("\n絵文字の検出処理開始")
   
   for text in texts:
       emojis = extract_emojis(text)
       if len(emojis) > 0:
           total_texts_with_emoji += 1
           count = len(emojis)
           
           # カウントと例の保存
           if count >= 5:
               emoji_counts['5+'] += 1
               if len(examples['5+']) < 3:
                   examples['5+'].append(text)
           else:
               emoji_counts[count] += 1
               if len(examples[count]) < 3:
                   examples[count].append(text)
   
   return {
       'total_texts': len(texts),
       'texts_with_emoji': total_texts_with_emoji,
       'emoji_counts': emoji_counts,
       'examples': examples
   }

# 全ファイルのリスト
csv_files = ['jp_1.csv', 'jp_2.csv', 'jp_3.csv', 'jp_4.csv']

# 全体の統計を保持する辞書
total_stats = {
   'total_texts': 0,
   'texts_with_emoji': 0,
   'emoji_counts': {1: 0, 2: 0, 3: 0, 4: 0, '5+': 0},
   'examples': {1: [], 2: [], 3: [], 4: [], '5+': []}
}

# 各ファイルの処理
for file in csv_files:
   try:
       print(f"\n=== {file} の処理 ===")
       
       if file == 'jp_3.csv':
           texts = process_special_csv(file)
       else:
           texts = process_regular_csv(file)
       
       stats = analyze_detailed_emoji_usage(texts)
       
       # 各ファイルの結果を表示
       print(f"\n{file} の分析結果:")
       print(f"総テキスト数: {stats['total_texts']}")
       print(f"絵文字を含むテキスト数: {stats['texts_with_emoji']}")
       if stats['texts_with_emoji'] > 0:
           for count in [1, 2, 3, 4, '5+']:
               percentage = (stats['emoji_counts'][count] / stats['texts_with_emoji']) * 100
               print(f"絵文字{count}個使用: {stats['emoji_counts'][count]} ({percentage:.1f}%)")
       
       # 全体の統計に加算
       total_stats['total_texts'] += stats['total_texts']
       total_stats['texts_with_emoji'] += stats['texts_with_emoji']
       for count in [1, 2, 3, 4, '5+']:
           total_stats['emoji_counts'][count] += stats['emoji_counts'][count]
           
       # 例を追加（最大3つまで）
       for count in [1, 2, 3, 4, '5+']:
           for example in stats['examples'][count]:
               if len(total_stats['examples'][count]) < 3:
                   total_stats['examples'][count].append(f"[{file}] {example}")

   except FileNotFoundError:
       print(f"警告: {file}が見つかりませんでした")
   except Exception as e:
       print(f"エラー: {file}の処理中にエラーが発生しました - {str(e)}")

# 全体の結果を表示
print("\n=== 全ファイルの合計結果 ===")
print(f"総テキスト数: {total_stats['total_texts']}")
print(f"絵文字を含むテキスト数: {total_stats['texts_with_emoji']}")
if total_stats['texts_with_emoji'] > 0:
   print("\n絵文字使用数の内訳:")
   for count in [1, 2, 3, 4, '5+']:
       percentage = (total_stats['emoji_counts'][count] / total_stats['texts_with_emoji']) * 100
       print(f"絵文字{count}個使用: {total_stats['emoji_counts'][count]} ({percentage:.1f}%)")
   
   print("\n=== 例 ===")
   for count in [1, 2, 3, 4, '5+']:
       print(f"\n絵文字{count}個使用の例:")
       for example in total_stats['examples'][count]:
           print(f"- {example}")