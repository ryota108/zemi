const express = require("express");
const { google } = require("googleapis");
const axios = require("axios");
const app = express();
const PORT = process.env.PORT || 3000;

// アクセストークンとリフレッシュトークンを設定
const accessToken =
  "";
const refreshToken =
  "";

const oauth2Client = new google.auth.OAuth2(
  "",
  "",
  "http://localhost:3000/oauth2callback"
);

oauth2Client.setCredentials({
  access_token: accessToken,
  refresh_token: refreshToken,
  token_type: "Bearer",
  scope: "https://www.googleapis.com/auth/spreadsheets",
});

// YouTube Data APIのエンドポイントを設定
const videoId = "OIBODIPC_8Y";
const apiUrl = `https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&videoId=${videoId}&key=AIzaSyARosqa5qlXOR0tARjoruTbtwlVymHvFnQ&maxResults=100&textFormat=plainText`;

const fetchCommentsWithPaging = async () => {
  let nextPageToken = "";
  const allComments = [];
  let pageCount = 1;

  console.log(`開始: VideoID ${videoId} のコメントを取得します...`);

  while (true) {
    console.log(`\nページ ${pageCount} の取得を開始...`);
    const url = nextPageToken ? `${apiUrl}&pageToken=${nextPageToken}` : apiUrl;
    
    try {
      const response = await axios.get(url);
      const comments = response.data.items.map((item) => ({
        comment: item.snippet.topLevelComment.snippet.textDisplay,
        likeCount: item.snippet.topLevelComment.snippet.likeCount,
        publishedAt: item.snippet.topLevelComment.snippet.publishedAt,
      }));

      console.log(`✓ ${comments.length} 件のコメントを取得しました`);
      console.log(`現在の総コメント数: ${allComments.length + comments.length}`);

      // 最新の取得コメントのサンプルを表示
      if (comments.length > 0) {
        console.log('\n最新の取得コメントサンプル:');
        console.log(`"${comments[0].comment.substring(0, 50)}${comments[0].comment.length > 50 ? '...' : ''}"`);
        console.log(`いいね数: ${comments[0].likeCount}`);
        console.log(`投稿日時: ${comments[0].publishedAt}`);
      }

      allComments.push(...comments);

      if (response.data.nextPageToken) {
        nextPageToken = response.data.nextPageToken;
        console.log('次のページが存在します。取得を継続...');
        pageCount++;
      } else {
        console.log('\n全てのページの取得が完了しました。');
        break;
      }
    } catch (error) {
      console.error(`\nエラーが発生しました (ページ ${pageCount}):`);
      console.error(error.response ? error.response.data : error.message);
      throw error;
    }
  }

  console.log(`\n取得完了: 合計 ${allComments.length} 件のコメントを取得しました`);
  return allComments;
};

app.get("/fetch-comments", async (req, res) => {
  console.log('コメント取得APIが呼び出されました');
  try {
    // YouTube Data APIからコメントを取得
    console.log('\nYouTubeからコメントの取得を開始...');
    const comments = await fetchCommentsWithPaging();
    
    // Google Sheetsに接続
    console.log('\nGoogle Sheetsへの接続を開始...');
    const sheets = google.sheets({ version: "v4", auth: oauth2Client });

    // コメントをスプレッドシートに書き込む
    console.log('スプレッドシートへの書き込みを開始...');
    await sheets.spreadsheets.values.append({
      spreadsheetId: "",
      range: "Sheet3!A:C",
      valueInputOption: "USER_ENTERED",
      requestBody: {
        values: comments.map((comment) => [
          comment.comment,
          comment.likeCount,
          comment.publishedAt,
        ]),
      },
    });

    console.log('スプレッドシートへの書き込みが完了しました');
    res.status(200).send(`処理が完了しました。${comments.length}件のコメントを取得し、スプレッドシートに書き込みました。`);
  } catch (error) {
    console.error("\n処理中にエラーが発生しました:");
    console.error("Error details:", error.response ? error.response.data : error.message);
    res.status(500).send("コメントの取得中にエラーが発生しました");
  }
});

app.listen(PORT, () => {
  console.log(`サーバーが起動しました - ポート ${PORT} で待機中`);
});