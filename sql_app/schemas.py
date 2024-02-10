from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

# チャットセッションを作成するためのスキーマ
class ChatSessionCreate(BaseModel):
    chat_name: str

# チャットメッセージを作成するためのスキーマ
class ChatMessageCreate(BaseModel):
    session_id: int
    content: str
    sender: str  # 'user' or 'assistant'

# チャットメッセージを読み取るためのスキーマ
class ChatMessage(BaseModel):
    id: int
    content: str
    created_at: datetime
    sender: str

    class Config:
        orm_mode = True

# チャットセッションとそのメッセージを読み取るためのスキーマ
class ChatSession(BaseModel):
    id: int
    chat_name: str
    created_at: datetime
    messages: List[ChatMessage] = []

    class Config:
        orm_mode = True

# ファイルアイテムの作成用スキーマ
class FileItemCreate(BaseModel):
    name: str
    description: str
    original_name: str

# ファイルアイテムの読み取り用スキーマ
class FileItem(BaseModel):
    id: int
    created_at: datetime
    name: str
    description: str
    file_path: str
    original_name: str

    class Config:
        orm_mode = True