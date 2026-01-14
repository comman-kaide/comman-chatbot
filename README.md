# 株式会社カンマン チャットボットシステム

Claude APIとRAG(Retrieval-Augmented Generation)を活用した、Webサイト埋め込み型のインテリジェントチャットボットシステムです。

## 📋 目次

- [システム概要](#システム概要)
- [主な機能](#主な機能)
- [技術スタック](#技術スタック)
- [プロジェクト構成](#プロジェクト構成)
- [セットアップ手順](#セットアップ手順)
- [デプロイ手順](#デプロイ手順)
- [使用方法](#使用方法)

## システム概要

株式会社カンマンのホームページに設置するチャットボットシステムです。訪問者の質問に対して、FAQデータやドキュメントを元にClaude AIが自動回答します。

### 主な機能

✅ **Webサイト埋め込み型チャットウィジェット**
- モダンで使いやすいチャットUI
- レスポンシブデザイン対応
- セッション管理による会話履歴保持

✅ **Claude API連携**
- Claude 3.5 Sonnetによる高品質な回答生成
- コンテキストを考慮した自然な対話

✅ **RAG (検索拡張生成)**
- ChromaDBによるベクトル検索
- FAQとドキュメントからの関連情報取得
- 高精度な回答生成

✅ **管理画面**
- FAQ管理 (作成・編集・削除)
- ドキュメント管理
- チャット履歴閲覧
- 認証機能付き

## 技術スタック

### バックエンド
- **Python 3.10+**
- **FastAPI** - 高速なWeb APIフレームワーク
- **Claude API (Anthropic)** - AI言語モデル
- **ChromaDB** - ベクトルデータベース
- **PostgreSQL** - リレーショナルデータベース
- **SQLAlchemy** - ORM

### フロントエンド
- **React 18** with TypeScript
- **Axios** - HTTP クライアント
- **Webpack** - バンドラー

### 管理画面
- **React 18** with TypeScript
- **React Router** - ルーティング
- **Tailwind CSS** - CSSフレームワーク
- **Vite** - ビルドツール

## プロジェクト構成

```
comman-chatbot/
├── backend/              # バックエンドAPI
│   ├── app/
│   │   ├── main.py      # FastAPIアプリケーション
│   │   ├── database.py  # データベースモデル
│   │   ├── chatbot.py   # チャットボットロジック
│   │   ├── rag.py       # RAGシステム
│   │   ├── auth.py      # 認証機能
│   │   └── schemas.py   # Pydanticスキーマ
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/            # チャットウィジェット
│   ├── src/
│   │   ├── ChatWidget.tsx
│   │   ├── ChatWidget.css
│   │   └── index.tsx
│   ├── package.json
│   └── webpack.config.js
│
├── admin/              # 管理画面
│   ├── src/
│   │   ├── App.tsx
│   │   ├── pages/
│   │   │   ├── Login.tsx
│   │   │   ├── Dashboard.tsx
│   │   │   ├── FAQManagement.tsx
│   │   │   ├── DocumentManagement.tsx
│   │   │   └── ChatHistory.tsx
│   │   └── main.tsx
│   └── package.json
│
├── embed-code.html     # ホームページ埋め込み用コード
└── README.md          # このファイル
```

## セットアップ手順

### 1. 前提条件

- Python 3.10以上
- Node.js 18以上
- PostgreSQL 13以上
- Anthropic API キー

### 2. バックエンドのセットアップ

```bash
cd backend

# 仮想環境の作成と有効化
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 依存関係のインストール
pip install -r requirements.txt --break-system-packages

# 環境変数の設定
cp .env.example .env
# .env ファイルを編集して以下を設定:
# - ANTHROPIC_API_KEY: Anthropic APIキー
# - DATABASE_URL: PostgreSQLの接続URL
# - SECRET_KEY: JWT用のシークレットキー

# データベースのセットアップ
# PostgreSQLでデータベースを作成
createdb comman_chatbot

# アプリケーションの起動
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### 3. フロントエンド(チャットウィジェット)のセットアップ

```bash
cd frontend

# 依存関係のインストール
npm install

# 開発サーバーの起動
npm run dev

# 本番用ビルド
npm run build
# dist/chatbot-widget.js が生成されます
```

### 4. 管理画面のセットアップ

```bash
cd admin

# 依存関係のインストール
npm install

# 環境変数の設定
# .env ファイルを作成:
echo "VITE_API_URL=http://localhost:8000" > .env

# 開発サーバーの起動
npm run dev

# 本番用ビルド
npm run build
```

### 5. 初期管理者ユーザーの作成

Pythonスクリプトで初期ユーザーを作成:

```python
# create_admin.py
from app.database import SessionLocal, User
from app.auth import get_password_hash

db = SessionLocal()
admin_user = User(
    username="admin",
    email="admin@comman.co.jp",
    hashed_password=get_password_hash("your_secure_password"),
    is_admin=True,
    is_active=True
)
db.add(admin_user)
db.commit()
print("管理者ユーザーを作成しました")
```

実行:
```bash
cd backend
python create_admin.py
```

## デプロイ手順

### バックエンドのデプロイ (Docker使用)

1. **Dockerfileの作成** (backend/Dockerfile)

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

2. **Docker Composeでのデプロイ**

```yaml
# docker-compose.yml
version: '3.8'

services:
  db:
    image: postgres:13
    environment:
      POSTGRES_DB: comman_chatbot
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: your_password
    volumes:
      - postgres_data:/var/lib/postgresql/data

  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://postgres:your_password@db:5432/comman_chatbot
      ANTHROPIC_API_KEY: your_api_key
      SECRET_KEY: your_secret_key
    depends_on:
      - db

volumes:
  postgres_data:
```

起動:
```bash
docker-compose up -d
```

### フロントエンドのデプロイ

1. ビルド:
```bash
cd frontend
npm run build
```

2. `dist/chatbot-widget.js` をCDNまたはWebサーバーにアップロード

3. ホームページに埋め込み:
```html
<script
  src="https://your-cdn.com/chatbot-widget.js"
  data-comman-chatbot
  data-api-url="https://api.comman.co.jp"
  async
></script>
```

### 管理画面のデプロイ

1. ビルド:
```bash
cd admin
npm run build
```

2. `dist/` フォルダの内容をWebサーバーにアップロード

## 使用方法

### 管理画面の使い方

1. **ログイン**
   - `https://your-domain.com/admin` にアクセス
   - 管理者ユーザー名とパスワードでログイン

2. **FAQ追加**
   - 「FAQ管理」ページを開く
   - 「+ FAQ追加」ボタンをクリック
   - 質問、回答、カテゴリを入力
   - 「保存」をクリック

3. **ドキュメント追加**
   - 「ドキュメント管理」ページを開く
   - 「+ ドキュメント追加」ボタンをクリック
   - タイトルと内容を入力
   - 「保存」をクリック

4. **チャット履歴確認**
   - 「チャット履歴」ページでユーザーとの会話を確認

### ホームページへの埋め込み

`embed-code.html` のコードをWebサイトの `</body>` タグの直前に貼り付けます。

## API エンドポイント

### 公開エンドポイント

- `POST /api/chat` - チャット送信

### 管理者エンドポイント (認証必要)

- `POST /api/auth/login` - ログイン
- `GET /api/auth/me` - 現在のユーザー情報
- `GET /api/admin/faqs` - FAQ一覧取得
- `POST /api/admin/faqs` - FAQ作成
- `PUT /api/admin/faqs/{id}` - FAQ更新
- `DELETE /api/admin/faqs/{id}` - FAQ削除
- `GET /api/admin/documents` - ドキュメント一覧取得
- `POST /api/admin/documents` - ドキュメント作成
- `PUT /api/admin/documents/{id}` - ドキュメント更新
- `DELETE /api/admin/documents/{id}` - ドキュメント削除
- `GET /api/admin/chat-history` - チャット履歴取得

## トラブルシューティング

### よくある問題

**Q: チャットボットが応答しない**
- Anthropic APIキーが正しく設定されているか確認
- バックエンドAPIが起動しているか確認
- ブラウザのコンソールでエラーを確認

**Q: 管理画面にログインできない**
- データベースに管理者ユーザーが作成されているか確認
- パスワードが正しいか確認

**Q: RAG検索が機能しない**
- ChromaDBのデータディレクトリが書き込み可能か確認
- FAQやドキュメントが正しく保存されているか確認

## ライセンス

Copyright © 2026 株式会社カンマン

## お問い合わせ

株式会社カンマン
- 電話: 088-611-2333
- 営業時間: 平日 9:30～18:00
- Webサイト: https://comman.co.jp/
