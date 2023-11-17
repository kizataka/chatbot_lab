from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
from .database import Base

# チャット履歴のデータモデルを定義するクラス
class ChatSession(Base):
    __tablename__ = 'chat_sessions'
    
    id = Column(Integer, primary_key=True, index=True)
    chat_name = Column(String, unique=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    messages = relationship("ChatMessage", back_populates="session")

# チャットメッセージのデータモデルを定義するクラス
class ChatMessage(Base):
    __tablename__ = 'chat_messages'
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey('chat_sessions.id'))
    content = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    sender = Column(String)  # 'user' or 'assistant'
    
    session = relationship("ChatSession", back_populates="messages")

# ファイルアイテムのデータモデルを定義するクラス
class FileItem(Base):
    __tablename__ = 'file_items'

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, default=datetime.utcnow)
    name = Column(String, index=True)
    description = Column(String)
    file_path = Column(String)
    original_name = Column(String)