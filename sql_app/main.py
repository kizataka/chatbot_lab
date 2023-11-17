from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Form
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List
from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def root():
    return {'message': 'Hello!'}

# チャット履歴をDBに登録
@app.post("/chat_sessions/", response_model=schemas.ChatSession)
def create_session(chat_session: schemas.ChatSessionCreate, db: Session = Depends(get_db)):
    db_chat_session = crud.create_chat_session(db, chat_session=chat_session)
    return db_chat_session

# チャット履歴の読み取り
@app.get("/chat_sessions/", response_model=List[schemas.ChatSession])
def read_sessions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    chat_sessions = crud.get_chat_sessions(db, skip=skip, limit=limit)
    return chat_sessions

# チャットメッセージをDBに登録
@app.post("/chat_messages/", response_model=schemas.ChatMessage)
def create_message(message: schemas.ChatMessageCreate, db: Session = Depends(get_db)):
    return crud.create_chat_message(db, message=message)

# チャットメッセージの取得
@app.get("/chat_messages/{session_id}", response_model=List[schemas.ChatMessage])
def read_messages(session_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    messages = crud.get_chat_messages(db, session_id=session_id, skip=skip, limit=limit)
    return messages

# チャット履歴の削除
@app.delete('/chat_sessions/{session_id}')
def delete_session(session_id: int, db: Session = Depends(get_db)):
    # 関連するメッセージを削除
    crud.delete_chat_messages_by_session(db, session_id=session_id)
    # セッションを削除
    db_session = crud.delete_chat_session(db, session_id=session_id)
    if db_session is None:
        raise HTTPException(status_code=404, detail='Session not found')
    return {'message': 'Session deleted successfully!'}

# ファイルデータをDBに登録
@app.post("/file_items/")
async def create_file_item(
    file: UploadFile = File(...),
    name: str = Form(...),
    description: str = Form(...),
    db: Session = Depends(get_db)
):
    # ここにファイルを保存し、データベースに情報を保存するロジックを実装
    file_location = f'files_{file.filename}'
    with open(file_location, 'wb') as file_object:
        file_object.write(await file.read())
    
    # データベースにファイル情報を保存
    file_item = schemas.FileItemCreate(name=name, description=description, original_name=file.filename, file_path=file_location)
    return crud.create_file_item(db=db, file_item=file_item, file_path=file_location, original_name=file.filename)

# アップロードされたファイルデータを全て取得
@app.get("/file_items/", response_model=list[schemas.FileItem])
def read_file_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    file_items = crud.get_file_items(db, skip=skip, limit=limit)
    return file_items

# ダウンロードするファイルデータを取得
@app.get("/file_items/download/{file_id}")
async def download_file(file_id: int, db: Session = Depends(get_db)):
    file_item = crud.get_file_item(db, file_item_id=file_id)
    if file_item is None:
        raise HTTPException(status_code=404, detail="File not found")
    file_path = file_item.file_path
    return FileResponse(path=file_path, filename=file_item.name)

# アップロードしたデータの削除
@app.delete("/file_items/{file_item_id}", response_model=schemas.FileItem)
def delete_file_item(file_item_id: int, db: Session = Depends(get_db)):
    db_file_item = crud.delete_file_item(db, file_item_id)
    if db_file_item is None:
        raise HTTPException(status_code=404, detail="File item not found")
    return db_file_item