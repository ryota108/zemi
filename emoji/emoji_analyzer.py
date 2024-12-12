import pandas as pd
import emoji

def count_emojis(text):
    if pd.isna(text):
        return 0
    return sum(emoji.is_emoji(char) for char in str(text))

def analyze_and_extract_emoji_rows(file_path):
    # CSVファイルを読み込む
    try:
        df = pd.read_csv(file_path, encoding='utf-8')
    except UnicodeDecodeError:
        df = pd.read_csv(file_path, encoding='cp932')
    
    # 元のデータフレームのインデックスを保持
    df['original_row'] = df.index + 1
    
    # 結果を格納するリスト
    results = []
    
    # 絵文字を含む行を抽出するためのマスク
    rows_with_emoji = pd.Series([False] * len(df))
    
    # 各列の全行をチェック
    for column in df.columns:
        if column == 'original_row':
            continue
            
        # 各行の絵文字をチェック
        emoji_counts = df[column].apply(count_emojis)
        rows_with_emoji |= (emoji_counts > 0)
        
        column_results = {
            'column_name': column,
            'total_emoji_count': emoji_counts.sum(),
            'rows_with_emoji': (emoji_counts > 0).sum()
        }
        results.append(column_results)
    
    # 絵文字を含む行だけを抽出
    emoji_df = df[rows_with_emoji].copy()
    
    # 集計結果のDataFrame
    summary_df = pd.DataFrame(results)
    
    return summary_df, emoji_df

if __name__ == "__main__":
    file_path = 'en.csv'
    summary_df, emoji_df = analyze_and_extract_emoji_rows(file_path)
    
    # 結果を保存
    summary_df.to_csv('emoji_summary.csv', index=False)
    emoji_df.to_csv('emoji_rows_only.csv', index=False)
    
    # 結果を表示
    print("\n=== 列ごとの絵文字集計 ===")
    print(summary_df)
    
    print(f"\n=== 絵文字を含む行の数: {len(emoji_df)} ===")
    print("\n=== 絵文字を含む行の最初の5行 ===")
    print(emoji_df.head())
    
    print(f"\n結果は以下のファイルに保存されました：")
    print("1. emoji_summary.csv - 列ごとの絵文字集計")
    print("2. emoji_rows_only.csv - 絵文字を含む行のみのデータ")