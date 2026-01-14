from fastapi import FastAPI, Depends, HTTPException, status, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import uuid
from datetime import timedelta

from app.config import settings
from app.database import get_db, init_db, FAQ, Document, ChatHistory, User
from app.schemas import (
    ChatRequest, ChatResponse, FAQCreate, FAQUpdate, FAQResponse,
    DocumentCreate, DocumentUpdate, DocumentResponse, UserCreate, UserResponse,
    LoginRequest, Token, ChatHistoryResponse
)
from app.chatbot import chatbot_service
from app.rag import rag_system
from app.auth import (
    get_password_hash, verify_password, create_access_token,
    get_current_user, get_current_active_admin_user
)

app = FastAPI(title="Comman Chatbot API", version="1.0.0")

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    """起動時にデータベースを初期化"""
    init_db()

# ============ Public Endpoints ============

@app.get("/")
def read_root():
    return {"message": "Comman Chatbot API", "version": "1.0.0"}

@app.post("/api/chat", response_model=ChatResponse)
def chat(request: ChatRequest, db: Session = Depends(get_db)):
    """チャットエンドポイント(認証不要)"""
    try:
        # セッションIDがない場合は生成
        session_id = request.session_id or str(uuid.uuid4())

        # 会話履歴を取得(最新5件)
        session_history = db.query(ChatHistory).filter(
            ChatHistory.session_id == session_id
        ).order_by(ChatHistory.created_at.desc()).limit(5).all()

        history_list = [
            {
                "user_message": h.user_message,
                "bot_response": h.bot_response
            }
            for h in reversed(session_history)
        ]

        # チャットボットの応答を生成
        response_text, context_used = chatbot_service.generate_response(
            request.message,
            history_list
        )

        # 会話履歴を保存
        chat_record = ChatHistory(
            session_id=session_id,
            user_message=request.message,
            bot_response=response_text,
            context_used={"contexts": context_used}
        )
        db.add(chat_record)
        db.commit()

        return ChatResponse(
            response=response_text,
            session_id=session_id,
            context_used=context_used
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"エラーが発生しました: {str(e)}")

# ============ Authentication ============

@app.post("/api/auth/login", response_model=Token)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    """ログイン"""
    user = db.query(User).filter(User.username == request.username).first()

    if not user or not verify_password(request.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="ユーザー名またはパスワードが正しくありません"
        )

    if not user.is_active:
        raise HTTPException(status_code=400, detail="ユーザーが無効です")

    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=timedelta(minutes=settings.access_token_expire_minutes)
    )

    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/api/auth/register", response_model=UserResponse)
def register(
    user: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_admin_user)
):
    """ユーザー登録(管理者のみ)"""
    # ユーザー名の重複チェック
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(status_code=400, detail="ユーザー名は既に使用されています")

    # メールアドレスの重複チェック
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="メールアドレスは既に使用されています")

    # 新規ユーザーを作成
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=get_password_hash(user.password)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

@app.get("/api/auth/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    """現在のユーザー情報を取得"""
    return current_user

# ============ FAQ Management (Admin) ============

@app.get("/api/admin/faqs", response_model=List[FAQResponse])
def list_faqs(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_admin_user)
):
    """FAQ一覧を取得"""
    faqs = db.query(FAQ).offset(skip).limit(limit).all()
    return faqs

@app.post("/api/admin/faqs", response_model=FAQResponse)
def create_faq(
    faq: FAQCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_admin_user)
):
    """FAQ を作成"""
    db_faq = FAQ(**faq.dict())
    db.add(db_faq)
    db.commit()
    db.refresh(db_faq)

    # RAGシステムに追加
    rag_system.add_document(
        text=f"質問: {faq.question}\n回答: {faq.answer}",
        metadata={"source": "FAQ", "category": faq.category, "id": db_faq.id},
        doc_id=f"faq_{db_faq.id}"
    )

    return db_faq

@app.put("/api/admin/faqs/{faq_id}", response_model=FAQResponse)
def update_faq(
    faq_id: int,
    faq: FAQUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_admin_user)
):
    """FAQを更新"""
    db_faq = db.query(FAQ).filter(FAQ.id == faq_id).first()
    if not db_faq:
        raise HTTPException(status_code=404, detail="FAQが見つかりません")

    # 更新
    for key, value in faq.dict(exclude_unset=True).items():
        setattr(db_faq, key, value)

    db.commit()
    db.refresh(db_faq)

    # RAGシステムを更新
    rag_system.update_document(
        doc_id=f"faq_{faq_id}",
        text=f"質問: {db_faq.question}\n回答: {db_faq.answer}",
        metadata={"source": "FAQ", "category": db_faq.category, "id": db_faq.id}
    )

    return db_faq

@app.delete("/api/admin/faqs/{faq_id}")
def delete_faq(
    faq_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_admin_user)
):
    """FAQを削除"""
    db_faq = db.query(FAQ).filter(FAQ.id == faq_id).first()
    if not db_faq:
        raise HTTPException(status_code=404, detail="FAQが見つかりません")

    db.delete(db_faq)
    db.commit()

    # RAGシステムから削除
    try:
        rag_system.delete_document(f"faq_{faq_id}")
    except:
        pass

    return {"message": "FAQを削除しました"}

# ============ Document Management (Admin) ============

@app.get("/api/admin/documents", response_model=List[DocumentResponse])
def list_documents(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_admin_user)
):
    """ドキュメント一覧を取得"""
    documents = db.query(Document).offset(skip).limit(limit).all()
    return documents

@app.post("/api/admin/documents", response_model=DocumentResponse)
def create_document(
    document: DocumentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_admin_user)
):
    """ドキュメントを作成"""
    db_doc = Document(**document.dict())
    db.add(db_doc)
    db.commit()
    db.refresh(db_doc)

    # RAGシステムに追加
    rag_system.add_document(
        text=f"タイトル: {document.title}\n内容: {document.content}",
        metadata={"source": "Document", "category": document.category, "id": db_doc.id},
        doc_id=f"doc_{db_doc.id}"
    )

    return db_doc

@app.put("/api/admin/documents/{doc_id}", response_model=DocumentResponse)
def update_document(
    doc_id: int,
    document: DocumentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_admin_user)
):
    """ドキュメントを更新"""
    db_doc = db.query(Document).filter(Document.id == doc_id).first()
    if not db_doc:
        raise HTTPException(status_code=404, detail="ドキュメントが見つかりません")

    # 更新
    for key, value in document.dict(exclude_unset=True).items():
        setattr(db_doc, key, value)

    db.commit()
    db.refresh(db_doc)

    # RAGシステムを更新
    rag_system.update_document(
        doc_id=f"doc_{doc_id}",
        text=f"タイトル: {db_doc.title}\n内容: {db_doc.content}",
        metadata={"source": "Document", "category": db_doc.category, "id": db_doc.id}
    )

    return db_doc

@app.delete("/api/admin/documents/{doc_id}")
def delete_document(
    doc_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_admin_user)
):
    """ドキュメントを削除"""
    db_doc = db.query(Document).filter(Document.id == doc_id).first()
    if not db_doc:
        raise HTTPException(status_code=404, detail="ドキュメントが見つかりません")

    db.delete(db_doc)
    db.commit()

    # RAGシステムから削除
    try:
        rag_system.delete_document(f"doc_{doc_id}")
    except:
        pass

    return {"message": "ドキュメントを削除しました"}

# ============ Chat History (Admin) ============

@app.get("/api/admin/chat-history", response_model=List[ChatHistoryResponse])
def list_chat_history(
    skip: int = 0,
    limit: int = 100,
    session_id: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_admin_user)
):
    """チャット履歴を取得"""
    query = db.query(ChatHistory)

    if session_id:
        query = query.filter(ChatHistory.session_id == session_id)

    history = query.order_by(ChatHistory.created_at.desc()).offset(skip).limit(limit).all()
    return history

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.host, port=settings.port)
