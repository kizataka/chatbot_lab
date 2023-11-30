# 研究室専用ChatBot

[![Python](https://img.shields.io/badge/Python-3.9.8-3776AB?logo=python&logoColor=3776AB)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-009688?logo=fastapi&logoColor=009688)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28.2-FF4B4B?logo=Streamlit&logoColor=FF4B4B)](https://streamlit.io/)
[![SQLite](https://img.shields.io/badge/SQLite-3.36-003B57?logo=sqlite&logoColor=003B57)](https://www.sqlite.org/index.html)
[![Poetry](https://img.shields.io/badge/Poetry-1.1.12-60A5FA?logo=Poetry&logoColor=60A5FA)](https://python-poetry.org/)

## サービス概要
研究室内の資料をChatGPTに学習させて研究関連の知識に特化させ、その内容について質問することができるチャットボットです。  

### ▼ サービスURL  
https://chatbot-for-lab.onrender.com  

### ▼ 紹介記事(Qiita)
開発背景など詳細な内容を記事にまとめる予定です。

### ▼ 作成理由
大学での研究活動の効率化が目的です。研究活動を進めるにおいて以下の課題がありました。
- 教授や先輩は忙しく、質問できる機会が限られておりなかなか疑問を解消することができない
- 簡単な質問はなんとなくしづらい、、、
- 研究内容は専門性が高く、webやChatGPTを使っても有効な答えを得られない
- ChatGPTの有料版でないとPDFファイルの内容を学習させることができない
- 無料で使えるChatPDFだと一つのファイルしか学習させることができず、回答範囲が狭い  

これらの課題を解決して研究活動を進めやすくなれればいいなと思い、研究室専用のチャットボットを作成しました。

## 使い方  
<table>
  <tr>
    <th style="text-align: center">チャットと履歴の閲覧</th>
    <th style="text-align: center">資料共有</th>
  </tr>
  <tr>
    <td><img src="https://github.com/kizataka/chatbot_lab/assets/112063667/e042399e-3ba6-43b2-9aa8-13b94751b083" alt="チャットと履歴の閲覧" />チャット名を入力してからチャットを開始します。チャット内容の履歴の閲覧と削除はHistoryページで確認できます。</td>
    <td><img src="https://github.com/kizataka/chatbot_lab/assets/112063667/8ac1a797-f841-4449-b32a-9e91483c886c" alt="資料共有" />資料をアップロードすることで資料を共有することができます。</td>
  </tr>
</table>

| チャットと履歴閲覧 |
| ---- |
| ![チャットと履歴閲覧画面](https://github.com/kizataka/chatbot_lab/assets/112063667/e042399e-3ba6-43b2-9aa8-13b94751b083) |
| チャット名を入力してからチャットを開始します。チャット内容の履歴の閲覧と削除はHistoryページで確認できます。 |


## 使用技術一覧  
**バックエンド**: Python 3.9.8 / FastAPI 0.104.1  

**フロントエンド**: Python 3.9.8 / Streamlit 1.28.2  
- PDFファイルの解析: OpenAI Embeddings API
- チャット: ChatGPT API

**データベース**: SQLite  

**環境構築**: Poetry  

**デプロイ**: Render.com  

## 機能一覧  
◆ チャット機能
- PDFファイルのアップロード機能
- ChatGPTAPIの機能を利用し、PDFファイルの内容をベクトル化する機能(OpenAI Embeddings API使用)
- Vector Store (Chroma) を利用してベクトル化された文章を保存・検索する機能
- アップロードされたファイルの内容に関してのチャット機能(ChatGPT API使用)

◆ チャット履歴閲覧機能
- チャット履歴の取得 / 作成 / 削除機能

◆ ファイル共有機能
- PDFファイルのアップロード機能
- 資料共有データの取得 / 作成 / 削除機能
- PDFファイルのダウンロード機能  

## ER図  
<img width="734" alt="ER図_chatbot_for_lab" src="https://github.com/kizataka/chatbot_lab/assets/112063667/4cfd1195-96d8-4d01-81f6-eb0a5d2c5131">