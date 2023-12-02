import os
import requests
import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
from io import BytesIO
from dotenv import load_dotenv

from langchain.document_loaders import PyPDFLoader
from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.indexes import VectorstoreIndexCreator
from langchain.chat_models import ChatOpenAI
from langchain.schema import (SystemMessage, HumanMessage, AIMessage)

# backend_url = 'http://127.0.0.1:8000'  # ローカル用
backend_url = 'https://chatbot-lab-backend.onrender.com'  # 本番用

# 環境変数の読み込み
load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')

def main():
    
    # ページの設定
    st.set_page_config(
        page_title='chatbot_for_lab',
        layout='wide'
    )

    # ページタイトル
    st.markdown('# 研究室用ChatBot')
    st.write('')

    # ページ構成
    selected = option_menu(
        menu_title=None,
        options=["Chat", "History", "Files"], 
        icons=['chat', 'book', "list-task"], 
        menu_icon="cast",
        default_index=0,
        orientation="horizontal")
    
    # 'chats'ページ
    if selected == 'Chat':
        st.markdown('## チャットページ')
        st.write('ここではpdfファイルをアップロードして独自のチャットボットを作成することができます')
        st.write('複数のpdfファイルをアップロードし、学習させることができます')
        st.write('独自のチャットボットを作成することで24時間質問対応が可能になります')
        st.write('')

        # チャット名の設定
        chat_name_input = st.text_input('チャットの名前を入力してください:', key='chat_name')

        if chat_name_input:
            if 'chat_name' not in st.session_state:
                chat_name_response = requests.get(f'{backend_url}/chat_sessions/')
                if chat_name_response.status_code == 200:
                    existing_sessions = chat_name_response.json()
                    # チャット名の重複確認
                    if any(chat_name_input == session['chat_name'] for session in existing_sessions):
                        st.warning('このチャット名は既に使用されています。別の名前を入力してください。')
                        st.stop()
                    else:
                        if 'chat_name' not in st.session_state or st.session_state['chat_name'] != chat_name_input:
                            st.session_state['chat_name'] = chat_name_input
                else:
                    st.error('チャット履歴の取得に失敗しました')

            chat_name = st.session_state['chat_name']

        else:
            st.warning('チャットを開始する前に、チャット名を入力してください')
            st.stop()

        # ファイルアップロード
        uploaded_files = st.file_uploader(
            label='botに学習させたいpdfファイルをアップロードしてください:',
            type='pdf',
            accept_multiple_files=True
        )

        # ファイルの読み込み
        if uploaded_files:
            docs = []
            for uploaded_file in uploaded_files:
                # ファイルを一時的に保存する
                with open(uploaded_file.name, 'wb') as f:
                    f.write(uploaded_file.getbuffer())

                # PDFローダーを使用して文書を読み込む
                loader = PyPDFLoader(uploaded_file.name)
                loaded_docs = loader.load()
                if loaded_docs:
                    docs.extend(loaded_docs)
                else:
                    st.error(f'Failed to load text from {uploaded_file.name}')

            if docs:
                # 文章のベクトル化
                index = VectorstoreIndexCreator(
                    vectorstore_cls=Chroma,
                    embedding=OpenAIEmbeddings(),
                ).from_documents(docs)

                if chat_name not in st.session_state:
                    st.session_state[chat_name] = [
                        SystemMessage(content='何でも聞いてね！')
                    ]

                # チャット画面の構成
                container = st.container()
                with container:
                    # メッセージ入力とメッセージ送信ボタンの実装
                    with st.form(key='my_form', clear_on_submit=True):
                        user_input = st.text_area(label='Message: ', key='input', height=100)
                        submit_button = st.form_submit_button(label='送信')

                    if submit_button and user_input:

                        # session_idがすでにあるかどうかの確認
                        if 'session_id' not in st.session_state or not st.session_state['session_id']:
                            session_response = requests.post(f'{backend_url}/chat_sessions/', json={
                                'chat_name': chat_name
                            })
                        
                            if session_response.status_code == 200:
                                session_data = session_response.json()
                                st.session_state['session_id'] = session_data['id']
                            else:
                                st.error('セッションを取得できませんでした。ステータスコード： {}'.format(session_response.status_code))
                                st.write(session_response.text)

                        # session_idを取得
                        session_id = st.session_state.get('session_id')

                        # ユーザー側のチャット内容を保存
                        post_response = requests.post(f'{backend_url}/chat_messages/', json={
                            'session_id': session_id,
                            'content': user_input,
                            'sender': 'user'
                        })

                        # チャット内容の保持
                        st.session_state[chat_name].append(HumanMessage(content=user_input))

                        if post_response.status_code == 200:
                            with st.spinner('ChatGPT is typing ...'):
                                pdf_response = index.query(user_input)

                            # チャット内容の保持
                            st.session_state[chat_name].append(AIMessage(content=pdf_response))
                            
                            # bot側のチャット内容を保存
                            assistant_response = requests.post(f'{backend_url}/chat_messages/', json={
                                'session_id': session_id,
                                'content': pdf_response,
                                'sender': 'assistant'
                            })

                            if assistant_response.status_code != 200:
                                st.error('アシスタントのメッセージの保存に失敗しました')
                                st.json(assistant_response.json())

                        else:
                            st.error('メッセージの保存に失敗しました。')
                            st.json(post_response.json())

                    # 今までのチャット内容を表示
                    messages = st.session_state.get(chat_name, [])
                    for message in messages:
                        if isinstance(message, AIMessage):
                            with st.chat_message('assistant'):
                                st.markdown(message.content)
                        elif isinstance(message, HumanMessage):
                            with st.chat_message('user'):
                                st.markdown(message.content)
                        else:
                            st.write(f"System message: {message.content}") 
    

    # 'history'ページ
    elif selected == 'History':
        st.markdown('## チャット履歴ページ')
        st.write('ここでは過去のチャットを閲覧することができます')
        st.write('')

        # 全てのチャット履歴の取得
        history_response = requests.get(f'{backend_url}/chat_sessions/')

        if history_response.status_code == 200:
            chat_sessions = history_response.json()
            if not chat_sessions:
                st.warning('履歴はありません')
            else:
                for session in chat_sessions:
                    with st.expander(f'チャット履歴：{session["chat_name"]}'):

                        # チャット履歴内の全てのメッセージを取得
                        messages_response = requests.get(f'{backend_url}/chat_messages/{session["id"]}')
                        if messages_response.status_code == 200:
                            messages = messages_response.json()
                            for message in messages:
                                st.write(f'{message["sender"]}: {message["content"]}')
                        else:
                            st.error('メッセージの取得に失敗しました')

                        # チャット履歴の削除
                        if st.button('このチャット履歴を削除', key=f'delete_{session["id"]}'):
                            # 対応するidのチャット履歴を削除
                            delete_response = requests.delete(f'{backend_url}/chat_sessions/{session["id"]}')
                            if delete_response.status_code == 200:
                                st.success('履歴が削除されました')
                            else:
                                st.error('履歴の削除に失敗しました。ステータスコード：{}'.format(delete_response.status_code))
                                st.text('レスポンスボディ：')
                                st.write(delete_response.text)
                            
        else:
            st.error('チャットセッションの取得に失敗しました')

    # 'files'ページ
    elif selected == 'Files':
        st.markdown('## 研究資料共有ページ')
        st.write('ここでは研究に関する資料を共有することができます')
        st.write('チャットボットの作成に必要なファイルがあればこちらからダウンロードすることができます')
        st.write('')

        # ファイルアップロード
        st.markdown('#### 資料のアップロードはここから')
        st.write('※アップロードに加えて、名前とファイルに関する説明文を入力してください')
        with st.form(key='file_ipload_form'):
            uploaded_file = st.file_uploader('pdfファイルをアップロードしてください:', type=['pdf'])
            name = st.text_input('名前:')
            description = st.text_area('ファイルに関する説明:')
        
            # ファイルのアップロード
            if st.form_submit_button('アップロード'):
                if uploaded_file is not None and name and description:
                    file_bytes = BytesIO(uploaded_file.getvalue())

                    files = {
                        'file': (uploaded_file.name, file_bytes, 'application/pdf'),
                        'name': (None, name),
                        'description': (None, description)
                    }

                    # アップロードしたファイルと詳細データを保存
                    data_response = requests.post(f'{backend_url}/file_items/', files=files)
                    
                    if data_response.status_code == 200:
                        st.success('ファイルがアップロードされました')
                    else:
                        st.error('ファイルのアップロードに失敗しました。ステータスコード:{}'.format(data_response.status_code))
                        st.text('レスポンスボディ:')
                        st.write(data_response.text)
                else:
                    st.warning('ファイル、名前、説明を入力してください')

        # ファイル一覧表示
        st.write('')
        st.markdown('#### 資料一覧')
        st.write('')

        # アップロードされたファイルデータを全て取得
        file_response = requests.get(f'{backend_url}/file_items/')
        if file_response.status_code == 200:
            file_items = file_response.json()

            # ファイルデータがアップロードされている場合
            if file_items:
                # DataFrameの作成
                df = pd.DataFrame(file_items)
                df['index'] = range(1, len(df) + 1)
                df = df[['index', 'id', 'name', 'description', 'original_name']]

                # カラム名の表示
                header_col1, header_col2, header_col3, header_col4, header_col5 = st.columns([0.5, 1.5, 4.5, 2, 1.5])
                header_col1.markdown('#### ID')
                header_col2.markdown('#### Name')
                header_col3.markdown('#### Description')
                header_col4.markdown('#### Download')
                header_col5.markdown('#### Delete')

                # 各行のデータ表示
                for index, row in df.iterrows():
                    col1, col2, col3, col4, col5 = st.columns([0.5, 1.5, 4.5, 2, 1.5])
                    col1.write(row['index'])
                    col2.write(row['name'])
                    col3.write(row['description'])

                    # ダウンロードするファイルデータの場所
                    download_url = f'{backend_url}/file_items/download/{row["id"]}'

                    # ファイルのダウンロード機能の実装
                    if col4.button('ダウンロード', key=f'download_{row["id"]}'):
                        # ダウンロードするファイルデータを取得
                        file_data = requests.get(download_url)
                        if file_data.status_code == 200:
                            # ダウンロード開始
                            btn = col4.download_button(
                                label='ダウンロード開始',
                                data=file_data.content,
                                file_name=row['original_name'],
                                mime='application/pdf'
                            )

                    # アップロードしたデータを削除する機能の実装
                    if col5.button('削除', key=f'delete_{row["id"]}'):
                        delete_response = requests.delete(f'{backend_url}/file_items/{row["id"]}')
                        if delete_response.status_code == 200:
                            st.success('ファイルが削除されました')
                        else:
                            st.error('ファイルの削除に失敗しました')
            
            # アップロードされているデータがない場合
            else:
                st.warning('現在アップロードされている資料はありません。')        


if __name__ == '__main__':
    main()