from sqlalchemy.orm import Session
from datetime import datetime
from . import models, schemas

# チャット履歴を作成する関数
def create_chat_session(db: Session, chat_session: schemas.ChatSessionCreate):
    db_chat_session = models.ChatSession(chat_name=chat_session.chat_name)
    db.add(db_chat_session)
    db.commit()
    db.refresh(db_chat_session)
    return db_chat_session

# 特定のチャット履歴を取得する関数
def get_chat_sessions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.ChatSession).offset(skip).limit(limit).all()

# チャットメッセージを作成する関数
def create_chat_message(db: Session, message: schemas.ChatMessageCreate):
    db_message = models.ChatMessage(**message.dict())
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

# 全てのチャット履歴を取得する関数
def get_chat_messages(db: Session, session_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.ChatMessage).filter(models.ChatMessage.session_id == session_id).offset(skip).limit(limit).all()

# 特定のチャット履歴のメッセージを削除する関数
def delete_chat_messages_by_session(db: Session, session_id: int):
    db.query(models.ChatMessage).filter(models.ChatMessage.session_id == session_id).delete()
    db.commit()

# 特定のチャット履歴を削除する関数
def delete_chat_session(db: Session, session_id: int):
    db_session = db.query(models.ChatSession).filter(models.ChatSession.id == session_id).first()
    if db_session:
        db.delete(db_session)
        db.commit()
        return db_session
    
# ファイルアイテムを作成する関数
def create_file_item(db: Session, file_item: schemas.FileItemCreate, file_path: str, original_name: str):
    db_item = models.FileItem(name=file_item.name, description=file_item.description, created_at=datetime.now(), file_path=file_path, original_name=original_name)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

# 全てのファイルアイテムを取得する関数
def get_file_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.FileItem).offset(skip).limit(limit).all()

# 特定のファイルアイテムを取得する関数
def get_file_item(db: Session, file_item_id: int):
    return db.query(models.FileItem).filter(models.FileItem.id == file_item_id).first()

# 特定のファイルアイテムを削除する関数
def delete_file_item(db: Session, file_item_id: int):
    db_item = db.query(models.FileItem).filter(models.FileItem.id == file_item_id).first()
    if db_item:
        db.delete(db_item)
        db.commit()
        return db_item