<img width="963" alt="ヘッダー画像" src="https://github.com/kizataka/chatbot_lab/assets/112063667/30ddd113-f76c-4c38-b436-8f2c920717b8">

[![Python](https://img.shields.io/badge/Python-v3.9.8-3776AB?logo=python&logoColor=3776AB)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-v0.85.1-009688?logo=fastapi&logoColor=009688)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-v1.28.2-FF4B4B?logo=Streamlit&logoColor=FF4B4B)](https://streamlit.io/)
[![SQLite](https://img.shields.io/badge/SQLite-gray?logo=sqlite&logoColor=003B57)](https://www.sqlite.org/index.html)
[![Poetry](https://img.shields.io/badge/Poetry-gray?logo=Poetry&logoColor=60A5FA)](https://python-poetry.org/)

## 概要 
### ▼ サイトURL  
https://chatbot-for-lab.onrender.com  

### ▼ 紹介記事(Qiita)
開発の経緯について以下の記事に詳細にまとめました。  
[大規模言語モデルLLMを活用したアプリ開発に挑戦！](https://qiita.com/kizataka/items/dfc26096a2248403964b)

### ▼ 作成理由
大学での研究活動の効率化が目的です。研究活動を進めるにおいて以下の課題がありました。
- 教授や先輩は忙しく、質問できる機会が限られておりなかなか疑問を解消することができない
- 簡単な質問はなんとなくしづらい、、、
- 研究内容は専門性が高く、webやChatGPTを使っても有効な答えを得られない
- ChatGPTの有料版でないとPDFファイルの内容を学習させることができない
- 無料で使えるChatPDFだと一つのファイルしか学習させることができず、回答範囲が狭い  

これらの課題を解決して研究活動を進めやすくなれればいいなと思い、研究室専用のチャットボットを作成しました。

## 使い方  

### チャットと履歴閲覧
![チャットと履歴閲覧](/app_view/demo_chat_history.gif)

チャット名を入力してからチャットを開始します。  
メッセージを入力して送信ボタンを押すとメッセージがポストされます。  
デモ動画では[2024年卒大学生就職企業人気ランキング](https://career-research.mynavi.jp/reserch/20230412_48385/)の内容についてチャットしています。    
「要約して」に対してしっかり回答が返ってくることがわかります。また、ソニーの得票数もしっかり合致しています。  
※APIのトークンの関係で英語で入力しています。

### 資料の共有
![資料共有](/app_view/demo_files.gif)

ここでは、教授や学生の間で資料が共有できるページになっています。  
アップロード欄からファイルをアップロードすることができます。  
アップロードした資料は資料一覧のところに保存されます。  
一覧にある資料をダウンロードしたいときはダウンロードボタンを、データを削除したい場合は削除ボタンを押します。

## 使用技術一覧  
**バックエンド**: Python 3.9.8 / FastAPI 0.85.1  

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
<img width="1089" alt="erd" src="https://github.com/kizataka/chatbot_lab/assets/112063667/2cd70d47-f7ee-46d9-af3b-aa8dd0145ee4">