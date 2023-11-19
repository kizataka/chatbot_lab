# 研究室専用ChatBot

## サービス概要
研究室内の資料をChatGPTに学習させ、その内容について質問することができるチャットボットです。

### ▼作成理由
大学での研究活動の効率化が目的です。研究活動を進めるにおいて以下の課題がありました。
- 教授や先輩は忙しく、質問できる機会が限られておりなかなか疑問を解消することができない

### ▼サービスURL  
https://chatbot-for-lab.onrender.com  

### ▼紹介記事(Qiita)


## 使い方  
デモ動画掲載  

[![Python](https://img.shields.io/badge/Python-3.9.8-3776AB?logo=python&logoColor=white)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28.2-FF4B4B?logo=Streamlit&logoColor=white)](https://streamlit.io/)
[![SQLite](https://img.shields.io/badge/SQLite-3.36-003B57?logo=sqlite&logoColor=white)](https://www.sqlite.org/index.html)
[![Poetry](https://img.shields.io/badge/Poetry-1.1.12-60A5FA?logo=Poetry&logoColor=white)](https://python-poetry.org/)

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

